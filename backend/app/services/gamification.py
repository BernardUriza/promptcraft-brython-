# PromptCraft - Gamification Service

from datetime import datetime, date
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.models.gamification import (
    UserGamification,
    XPTransaction,
    XPSource,
    Badge,
    UserBadge
)
from app.services.leaderboard import LeaderboardService
from app.services.badge import BadgeService
from app.config import settings


class GamificationService:
    """
    Central service for all gamification logic.
    Handles XP, levels, streaks, and daily goals.
    """

    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis
        self.leaderboard = LeaderboardService(redis, db)
        self.badge_service = BadgeService(db)

    async def award_xp(
        self,
        user_id: int,
        amount: int,
        source: XPSource,
        source_id: Optional[str] = None,
        description: Optional[str] = None,
        multiplier: float = 1.0
    ) -> dict:
        """
        Award XP to a user.

        Returns dict with:
        - xp_earned: Actual XP earned (after multiplier)
        - total_xp: New total XP
        - previous_level: Level before award
        - new_level: Level after award
        - level_up: Whether user leveled up
        - daily_xp_earned: Total XP earned today
        - daily_goal_completed: Whether daily goal was just completed
        - new_badges: List of newly earned badges
        """
        # Get user's gamification record
        result = await self.db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == user_id)
        )
        gamification = result.scalar_one_or_none()

        if not gamification:
            raise ValueError(f"No gamification record for user {user_id}")

        # Calculate actual XP
        actual_xp = int(amount * multiplier)
        previous_level = gamification.level
        previous_total = gamification.total_xp

        # Update XP
        gamification.total_xp += actual_xp
        gamification.daily_xp_earned += actual_xp
        gamification.updated_at = datetime.utcnow()

        # Calculate new level
        new_level = self._calculate_level(gamification.total_xp)
        level_up = new_level > previous_level
        gamification.level = new_level

        # Update streak
        await self._update_streak(gamification)

        # Check daily goal
        daily_goal_just_completed = (
            gamification.daily_xp_earned >= gamification.daily_xp_goal and
            gamification.daily_xp_earned - actual_xp < gamification.daily_xp_goal
        )

        if daily_goal_just_completed:
            gamification.daily_goal_streak += 1

        # Create XP transaction
        transaction = XPTransaction(
            user_id=user_id,
            amount=actual_xp,
            source=source,
            source_id=source_id,
            multiplier=multiplier,
            description=description,
            created_at=datetime.utcnow()
        )
        self.db.add(transaction)

        # Update leaderboards
        await self.leaderboard.update_user_score(user_id, actual_xp)

        # Check for new badges
        new_badges = await self.badge_service.check_badges(user_id, gamification)

        await self.db.commit()

        return {
            "xp_earned": actual_xp,
            "total_xp": gamification.total_xp,
            "previous_level": previous_level,
            "new_level": new_level,
            "level_up": level_up,
            "daily_xp_earned": gamification.daily_xp_earned,
            "daily_goal_completed": daily_goal_just_completed,
            "new_badges": new_badges
        }

    async def _update_streak(self, gamification: UserGamification):
        """Update user's streak based on activity."""
        today = date.today()
        last_activity = gamification.last_activity_date

        if last_activity is None:
            # First activity ever
            gamification.current_streak = 1
            gamification.longest_streak = 1
        elif last_activity == today:
            # Already active today, no change
            pass
        elif last_activity == today - date.resolution:
            # Active yesterday, continue streak
            gamification.current_streak += 1
            if gamification.current_streak > gamification.longest_streak:
                gamification.longest_streak = gamification.current_streak
        else:
            # Streak broken
            gamification.current_streak = 1

        gamification.last_activity_date = today

    def _calculate_level(self, total_xp: int) -> int:
        """Calculate level from total XP."""
        level = 1
        xp_remaining = total_xp

        while True:
            xp_for_next = self._xp_for_level(level + 1)
            if xp_remaining < xp_for_next:
                return level
            xp_remaining -= xp_for_next
            level += 1

    def _xp_for_level(self, level: int) -> int:
        """Calculate XP required to reach a level."""
        return int(settings.BASE_XP_PER_LEVEL * (settings.XP_MULTIPLIER ** (level - 1)))

    async def get_level_info(self, total_xp: int) -> dict:
        """
        Get detailed level information.

        Returns:
        - level: Current level
        - xp_in_level: XP earned in current level
        - xp_to_next: XP needed for next level
        - progress_percent: Progress to next level (0-100)
        """
        level = 1
        xp_remaining = total_xp

        while True:
            xp_for_next = self._xp_for_level(level + 1)
            if xp_remaining < xp_for_next:
                progress = int((xp_remaining / xp_for_next) * 100)
                return {
                    "level": level,
                    "xp_in_level": xp_remaining,
                    "xp_to_next": xp_for_next,
                    "progress_percent": progress
                }
            xp_remaining -= xp_for_next
            level += 1

    async def check_and_reset_daily(self, user_id: int):
        """
        Check if daily XP should be reset (new day).
        Called on user activity.
        """
        result = await self.db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == user_id)
        )
        gamification = result.scalar_one_or_none()

        if not gamification:
            return

        today = date.today()
        last_activity = gamification.last_activity_date

        if last_activity and last_activity < today:
            # New day, reset daily XP
            gamification.daily_xp_earned = 0
            await self.db.commit()

    async def use_streak_freeze(self, user_id: int) -> bool:
        """
        Use a streak freeze to prevent streak loss.

        Returns True if freeze was used successfully.
        """
        result = await self.db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == user_id)
        )
        gamification = result.scalar_one_or_none()

        if not gamification or gamification.streak_freezes <= 0:
            return False

        today = date.today()
        if gamification.last_activity_date == today:
            # Already active today
            return False

        gamification.streak_freezes -= 1
        gamification.last_activity_date = today
        await self.db.commit()

        return True

    async def get_streak_info(self, user_id: int) -> dict:
        """Get detailed streak information."""
        result = await self.db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == user_id)
        )
        gamification = result.scalar_one_or_none()

        if not gamification:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "streak_freezes": 0,
                "is_at_risk": False
            }

        today = date.today()
        is_at_risk = (
            gamification.last_activity_date is not None and
            gamification.last_activity_date < today and
            gamification.current_streak > 0
        )

        return {
            "current_streak": gamification.current_streak,
            "longest_streak": gamification.longest_streak,
            "streak_freezes": gamification.streak_freezes,
            "last_activity_date": gamification.last_activity_date,
            "is_at_risk": is_at_risk
        }
