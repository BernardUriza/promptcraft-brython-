# PromptCraft - Gamification Schemas

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

from app.models.gamification import BadgeRarity, BadgeCategory, XPSource


class GamificationStatsResponse(BaseModel):
    """User gamification stats response."""
    user_id: int

    # XP & Level
    total_xp: int = 0
    level: int = 1
    xp_in_current_level: int = 0
    xp_to_next_level: int = 100
    level_progress_percent: int = 0

    # Streak
    current_streak: int = 0
    longest_streak: int = 0
    streak_freezes: int = 0
    last_activity_date: Optional[date] = None
    streak_at_risk: bool = False  # True if no activity today

    # Stats
    lessons_completed: int = 0
    puzzles_completed: int = 0
    puzzles_3_stars: int = 0
    total_time_minutes: int = 0

    # Daily goals
    daily_xp_goal: int = 50
    daily_xp_earned: int = 0
    daily_goal_completed: bool = False
    daily_goal_streak: int = 0

    # Badges
    badges_earned: int = 0
    badges_total: int = 0

    model_config = {"from_attributes": True}


class XPTransactionResponse(BaseModel):
    """XP transaction response schema."""
    id: int
    amount: int
    source: XPSource
    source_id: Optional[str] = None
    multiplier: float = 1.0
    description: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class XPTransactionList(BaseModel):
    """Paginated XP transactions list."""
    items: list[XPTransactionResponse]
    total: int
    page: int
    per_page: int


class XPAwardResponse(BaseModel):
    """Response when XP is awarded."""
    xp_earned: int
    total_xp: int
    previous_level: int
    new_level: int
    level_up: bool = False
    daily_xp_earned: int
    daily_goal_completed: bool = False
    new_badges: list["BadgeResponse"] = []


class BadgeCondition(BaseModel):
    """Badge unlock condition schema."""
    type: str  # lessons_completed, puzzles_completed, streak, xp, etc.
    value: int
    operator: str = "gte"  # gte, lte, eq


class BadgeResponse(BaseModel):
    """Badge response schema."""
    id: int
    slug: str
    name: str
    description: str
    icon: str
    category: BadgeCategory
    rarity: BadgeRarity
    xp_reward: int = 0
    is_hidden: bool = False

    # User-specific
    is_earned: bool = False
    earned_at: Optional[datetime] = None
    progress: int = 0  # 0-100
    progress_current: int = 0
    progress_target: int = 0

    model_config = {"from_attributes": True}


class UserBadgeResponse(BaseModel):
    """User earned badge response."""
    badge: BadgeResponse
    earned_at: datetime
    notified: bool = False

    model_config = {"from_attributes": True}


class BadgeListResponse(BaseModel):
    """Badge list response."""
    earned: list[UserBadgeResponse]
    available: list[BadgeResponse]
    hidden_count: int = 0


class LeaderboardEntry(BaseModel):
    """Leaderboard entry schema."""
    rank: int
    user_id: int
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    score: int  # XP or other metric
    level: int = 1
    is_current_user: bool = False

    model_config = {"from_attributes": True}


class LeaderboardResponse(BaseModel):
    """Leaderboard response schema."""
    type: str  # daily, weekly, monthly, all_time
    entries: list[LeaderboardEntry]
    current_user_rank: Optional[int] = None
    current_user_entry: Optional[LeaderboardEntry] = None
    total_users: int
    last_updated: datetime


class DailyChallengeResponse(BaseModel):
    """Daily challenge response schema."""
    id: int
    challenge_date: date
    challenge_type: str
    target_id: Optional[int] = None
    target_count: int = 1
    xp_reward: int = 50
    title: str
    description: str

    # User-specific
    progress: int = 0
    is_completed: bool = False
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class StreakResponse(BaseModel):
    """Streak status response."""
    current_streak: int
    longest_streak: int
    streak_freezes: int
    last_activity_date: Optional[date] = None
    streak_at_risk: bool = False
    days_until_freeze_expires: Optional[int] = None
    streak_milestones: list[int] = [7, 30, 100, 365]
    next_milestone: Optional[int] = None
    days_to_next_milestone: Optional[int] = None


class StreakFreezeRequest(BaseModel):
    """Request to use streak freeze."""
    pass  # No parameters needed


class DailyGoalUpdate(BaseModel):
    """Update daily XP goal."""
    daily_xp_goal: int = Field(ge=10, le=500)
