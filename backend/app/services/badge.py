# PromptCraft - Badge Service

import json
from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gamification import (
    Badge,
    UserBadge,
    UserGamification,
    XPTransaction,
    XPSource
)


class BadgeService:
    """
    Service for managing badge awards and progress tracking.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_badges(
        self,
        user_id: int,
        gamification: UserGamification
    ) -> list[dict]:
        """
        Check all badge conditions and award any newly earned badges.

        Returns list of newly earned badges.
        """
        # Get all badges
        result = await self.db.execute(select(Badge))
        all_badges = result.scalars().all()

        # Get user's existing badges
        earned_result = await self.db.execute(
            select(UserBadge.badge_id)
            .where(UserBadge.user_id == user_id)
        )
        earned_badge_ids = {row[0] for row in earned_result.all()}

        new_badges = []

        for badge in all_badges:
            if badge.id in earned_badge_ids:
                continue

            if self._check_condition(badge, gamification):
                # Award badge
                user_badge = UserBadge(
                    user_id=user_id,
                    badge_id=badge.id,
                    earned_at=datetime.utcnow(),
                    notified=False
                )
                self.db.add(user_badge)

                # Award XP reward
                if badge.xp_reward > 0:
                    transaction = XPTransaction(
                        user_id=user_id,
                        amount=badge.xp_reward,
                        source=XPSource.BADGE_REWARD,
                        source_id=str(badge.id),
                        description=f"Badge earned: {badge.name}",
                        created_at=datetime.utcnow()
                    )
                    self.db.add(transaction)
                    gamification.total_xp += badge.xp_reward

                new_badges.append({
                    "id": badge.id,
                    "slug": badge.slug,
                    "name": badge.name,
                    "description": badge.description,
                    "icon": badge.icon,
                    "rarity": badge.rarity.value,
                    "xp_reward": badge.xp_reward
                })

        return new_badges

    def _check_condition(self, badge: Badge, gamification: UserGamification) -> bool:
        """Check if badge condition is met."""
        try:
            condition = json.loads(badge.condition)
        except (json.JSONDecodeError, TypeError):
            return False

        condition_type = condition.get("type", "")
        value = condition.get("value", 0)
        operator = condition.get("operator", "gte")

        current_value = self._get_current_value(condition_type, gamification)

        if operator == "gte":
            return current_value >= value
        elif operator == "gt":
            return current_value > value
        elif operator == "eq":
            return current_value == value
        elif operator == "lte":
            return current_value <= value
        elif operator == "lt":
            return current_value < value

        return False

    def _get_current_value(
        self,
        condition_type: str,
        gamification: UserGamification
    ) -> int:
        """Get current value for a condition type."""
        mapping = {
            "lessons_completed": gamification.lessons_completed,
            "puzzles_completed": gamification.puzzles_completed,
            "puzzles_3_stars": gamification.puzzles_3_stars,
            "current_streak": gamification.current_streak,
            "longest_streak": gamification.longest_streak,
            "total_xp": gamification.total_xp,
            "level": gamification.level,
            "daily_goal_streak": gamification.daily_goal_streak,
            "total_time_minutes": gamification.total_time_minutes
        }
        return mapping.get(condition_type, 0)

    async def get_badge_progress(
        self,
        user_id: int,
        badge_id: int
    ) -> Optional[dict]:
        """Get progress towards a specific badge."""
        # Get badge
        result = await self.db.execute(
            select(Badge).where(Badge.id == badge_id)
        )
        badge = result.scalar_one_or_none()

        if not badge:
            return None

        # Check if already earned
        earned_result = await self.db.execute(
            select(UserBadge)
            .where(UserBadge.user_id == user_id)
            .where(UserBadge.badge_id == badge_id)
        )
        user_badge = earned_result.scalar_one_or_none()

        if user_badge:
            return {
                "badge_id": badge_id,
                "is_earned": True,
                "earned_at": user_badge.earned_at,
                "progress": 100,
                "current_value": None,
                "target_value": None
            }

        # Get user's gamification
        gam_result = await self.db.execute(
            select(UserGamification)
            .where(UserGamification.user_id == user_id)
        )
        gamification = gam_result.scalar_one_or_none()

        if not gamification:
            return None

        # Calculate progress
        try:
            condition = json.loads(badge.condition)
        except:
            condition = {"type": "unknown", "value": 0}

        condition_type = condition.get("type", "")
        target_value = condition.get("value", 0)
        current_value = self._get_current_value(condition_type, gamification)

        progress = min(100, int((current_value / target_value) * 100)) if target_value > 0 else 0

        return {
            "badge_id": badge_id,
            "is_earned": False,
            "earned_at": None,
            "progress": progress,
            "current_value": current_value,
            "target_value": target_value
        }

    async def mark_badge_notified(self, user_id: int, badge_id: int):
        """Mark a badge notification as seen."""
        result = await self.db.execute(
            select(UserBadge)
            .where(UserBadge.user_id == user_id)
            .where(UserBadge.badge_id == badge_id)
        )
        user_badge = result.scalar_one_or_none()

        if user_badge:
            user_badge.notified = True
            await self.db.commit()
