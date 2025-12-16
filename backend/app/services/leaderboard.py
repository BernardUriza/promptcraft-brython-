# PromptCraft - Leaderboard Service (Redis ZSET)

from datetime import datetime, date, timedelta
from typing import Optional
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import RedisKeys
from app.models.user import User
from app.models.gamification import UserGamification, XPTransaction
from app.schemas.gamification import LeaderboardEntry, LeaderboardResponse


class LeaderboardService:
    """
    Service for managing leaderboards using Redis Sorted Sets (ZSET).

    Uses Redis ZSET for O(log N) insertions and O(log N + M) range queries.
    """

    def __init__(self, redis: Redis, db: AsyncSession):
        self.redis = redis
        self.db = db

    async def update_user_score(
        self,
        user_id: int,
        xp_amount: int,
        leaderboard_types: list[str] = None
    ):
        """
        Update user's score in leaderboards.

        Args:
            user_id: User ID
            xp_amount: XP to add (can be negative)
            leaderboard_types: Types to update (default: all)
        """
        if leaderboard_types is None:
            leaderboard_types = ["daily", "weekly", "monthly", "all_time"]

        today = date.today()

        for lb_type in leaderboard_types:
            key = self._get_leaderboard_key(lb_type, today)

            # ZINCRBY - increment score in sorted set
            await self.redis.zincrby(key, xp_amount, str(user_id))

            # Set expiry for time-limited leaderboards
            if lb_type == "daily":
                # Expire at midnight
                await self.redis.expireat(
                    key,
                    datetime.combine(today + timedelta(days=1), datetime.min.time())
                )
            elif lb_type == "weekly":
                # Expire at end of week
                days_until_sunday = 6 - today.weekday()
                await self.redis.expireat(
                    key,
                    datetime.combine(today + timedelta(days=days_until_sunday + 1), datetime.min.time())
                )
            elif lb_type == "monthly":
                # Expire at end of month
                if today.month == 12:
                    next_month = today.replace(year=today.year + 1, month=1, day=1)
                else:
                    next_month = today.replace(month=today.month + 1, day=1)
                await self.redis.expireat(key, datetime.combine(next_month, datetime.min.time()))

    async def get_leaderboard(
        self,
        leaderboard_type: str,
        current_user_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> LeaderboardResponse:
        """
        Get leaderboard entries.

        Args:
            leaderboard_type: daily, weekly, monthly, or all_time
            current_user_id: Current user ID (to mark their entry)
            limit: Number of entries to return
            offset: Starting position

        Returns:
            LeaderboardResponse with entries and current user info
        """
        today = date.today()
        key = self._get_leaderboard_key(leaderboard_type, today)

        # Get total count
        total_users = await self.redis.zcard(key)

        # Get top entries with scores (ZREVRANGE - descending order)
        entries_raw = await self.redis.zrevrange(
            key,
            offset,
            offset + limit - 1,
            withscores=True
        )

        # Get current user's rank if provided
        current_user_rank = None
        current_user_entry = None

        if current_user_id:
            # ZREVRANK - get rank in descending order (0-indexed)
            rank = await self.redis.zrevrank(key, str(current_user_id))
            if rank is not None:
                current_user_rank = rank + 1  # 1-indexed

                # Get user's score
                score = await self.redis.zscore(key, str(current_user_id))

                # Fetch user details
                result = await self.db.execute(
                    select(User).where(User.id == current_user_id)
                )
                user = result.scalar_one_or_none()

                if user:
                    current_user_entry = LeaderboardEntry(
                        rank=current_user_rank,
                        user_id=user.id,
                        username=user.username,
                        display_name=user.display_name,
                        avatar_url=user.avatar_url,
                        score=int(score) if score else 0,
                        level=1,  # Would need to fetch from gamification
                        is_current_user=True
                    )

        # Fetch user details for all entries
        entries = []
        user_ids = [int(uid) for uid, _ in entries_raw]

        if user_ids:
            result = await self.db.execute(
                select(User, UserGamification)
                .join(UserGamification)
                .where(User.id.in_(user_ids))
            )
            user_data = {u.id: (u, g) for u, g in result.all()}

            for rank, (user_id_bytes, score) in enumerate(entries_raw, start=offset + 1):
                user_id = int(user_id_bytes)
                if user_id in user_data:
                    user, gam = user_data[user_id]
                    entries.append(LeaderboardEntry(
                        rank=rank,
                        user_id=user.id,
                        username=user.username,
                        display_name=user.display_name,
                        avatar_url=user.avatar_url,
                        score=int(score),
                        level=gam.level if gam else 1,
                        is_current_user=user.id == current_user_id
                    ))

        return LeaderboardResponse(
            type=leaderboard_type,
            entries=entries,
            current_user_rank=current_user_rank,
            current_user_entry=current_user_entry,
            total_users=total_users,
            last_updated=datetime.utcnow()
        )

    async def rebuild_leaderboard(self, leaderboard_type: str):
        """
        Rebuild leaderboard from database.

        Used for initial setup or recovery.
        """
        today = date.today()
        key = self._get_leaderboard_key(leaderboard_type, today)

        # Clear existing leaderboard
        await self.redis.delete(key)

        # Determine date range
        if leaderboard_type == "daily":
            start_date = today
        elif leaderboard_type == "weekly":
            start_date = today - timedelta(days=today.weekday())
        elif leaderboard_type == "monthly":
            start_date = today.replace(day=1)
        else:
            start_date = None  # All time

        # Query XP transactions
        query = (
            select(
                XPTransaction.user_id,
                func.sum(XPTransaction.amount).label("total_xp")
            )
            .group_by(XPTransaction.user_id)
        )

        if start_date:
            query = query.where(XPTransaction.created_at >= datetime.combine(start_date, datetime.min.time()))

        from sqlalchemy import func
        result = await self.db.execute(query)

        # Add to Redis ZSET
        for user_id, total_xp in result.all():
            await self.redis.zadd(key, {str(user_id): total_xp})

    def _get_leaderboard_key(self, leaderboard_type: str, today: date) -> str:
        """Get Redis key for leaderboard type."""
        if leaderboard_type == "daily":
            return RedisKeys.leaderboard(f"daily:{today.isoformat()}")
        elif leaderboard_type == "weekly":
            week_start = today - timedelta(days=today.weekday())
            return RedisKeys.leaderboard(f"weekly:{week_start.isoformat()}")
        elif leaderboard_type == "monthly":
            return RedisKeys.leaderboard(f"monthly:{today.year}-{today.month:02d}")
        else:
            return RedisKeys.leaderboard("all_time")
