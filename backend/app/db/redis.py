# PromptCraft - Redis Connection Management
# For caching, leaderboards, and real-time features

from typing import Optional
import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.config import settings


# Global Redis connection
redis_client: Optional[Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection."""
    global redis_client

    redis_client = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=10
    )

    # Test connection
    await redis_client.ping()


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_redis() -> Redis:
    """
    Dependency that provides Redis connection.
    Use with FastAPI's Depends().
    """
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client


# Leaderboard keys
class RedisKeys:
    """Redis key patterns for the application."""

    # Leaderboards (Sorted Sets)
    LEADERBOARD_DAILY = "leaderboard:daily:{date}"
    LEADERBOARD_WEEKLY = "leaderboard:weekly:{week}"
    LEADERBOARD_ALLTIME = "leaderboard:alltime"

    # User sessions
    USER_SESSION = "session:{user_id}"

    # Rate limiting
    RATE_LIMIT = "ratelimit:{user_id}:{endpoint}"

    # Cache
    CACHE_USER = "cache:user:{user_id}"
    CACHE_LESSON = "cache:lesson:{lesson_id}"
    CACHE_PUZZLE = "cache:puzzle:{puzzle_id}"

    # Real-time
    ONLINE_USERS = "online_users"
    RECENT_ACTIVITIES = "activities:recent"

    # Streaks
    USER_STREAK = "streak:{user_id}"

    @classmethod
    def daily_leaderboard(cls, date: str) -> str:
        return cls.LEADERBOARD_DAILY.format(date=date)

    @classmethod
    def weekly_leaderboard(cls, week: str) -> str:
        return cls.LEADERBOARD_WEEKLY.format(week=week)

    @classmethod
    def user_session(cls, user_id: int) -> str:
        return cls.USER_SESSION.format(user_id=user_id)

    @classmethod
    def rate_limit(cls, user_id: int, endpoint: str) -> str:
        return cls.RATE_LIMIT.format(user_id=user_id, endpoint=endpoint)
