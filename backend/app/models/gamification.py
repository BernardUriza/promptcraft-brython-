# PromptCraft - Gamification Models

from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, DateTime, Date, ForeignKey, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User


class BadgeRarity(str, enum.Enum):
    """Rarity levels for badges."""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class BadgeCategory(str, enum.Enum):
    """Categories for badges."""
    PROGRESS = "progress"
    PUZZLES = "puzzles"
    STREAK = "streak"
    XP = "xp"
    LEVELS = "levels"
    SPECIAL = "special"


class XPSource(str, enum.Enum):
    """Sources of XP."""
    LESSON_COMPLETE = "lesson_complete"
    PUZZLE_COMPLETE = "puzzle_complete"
    EXERCISE_COMPLETE = "exercise_complete"
    DAILY_GOAL = "daily_goal"
    STREAK_BONUS = "streak_bonus"
    BADGE_REWARD = "badge_reward"
    CHALLENGE_COMPLETE = "challenge_complete"
    ACHIEVEMENT = "achievement"


class UserGamification(Base):
    """User gamification stats."""

    __tablename__ = "user_gamification"

    # User reference (one-to-one)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    # XP & Level
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)

    # Streak
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    streak_freezes: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_date: Mapped[Optional[date]] = mapped_column(Date)

    # Stats
    lessons_completed: Mapped[int] = mapped_column(Integer, default=0)
    puzzles_completed: Mapped[int] = mapped_column(Integer, default=0)
    puzzles_3_stars: Mapped[int] = mapped_column(Integer, default=0)
    total_time_minutes: Mapped[int] = mapped_column(Integer, default=0)

    # Daily goals
    daily_xp_goal: Mapped[int] = mapped_column(Integer, default=50)
    daily_xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    daily_goal_streak: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="gamification")

    def __repr__(self) -> str:
        return f"<UserGamification(user_id={self.user_id}, level={self.level}, xp={self.total_xp})>"


class XPTransaction(Base):
    """Record of XP transactions."""

    __tablename__ = "xp_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # User reference
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    # Transaction data
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[XPSource] = mapped_column(Enum(XPSource))
    source_id: Mapped[Optional[str]] = mapped_column(String(100))  # lesson_id, puzzle_id, etc.
    multiplier: Mapped[float] = mapped_column(Float, default=1.0)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="xp_transactions")

    def __repr__(self) -> str:
        return f"<XPTransaction(user_id={self.user_id}, amount={self.amount}, source='{self.source}')>"


class Badge(Base):
    """Badge definitions."""

    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Identification
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Display
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(10), default="🏆")

    # Classification
    category: Mapped[BadgeCategory] = mapped_column(Enum(BadgeCategory))
    rarity: Mapped[BadgeRarity] = mapped_column(
        Enum(BadgeRarity),
        default=BadgeRarity.COMMON
    )

    # Requirements (JSON)
    condition: Mapped[str] = mapped_column(Text)  # JSON with condition type and value

    # Reward
    xp_reward: Mapped[int] = mapped_column(Integer, default=0)

    # Metadata
    is_hidden: Mapped[bool] = mapped_column(default=False)
    order: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<Badge(id={self.id}, name='{self.name}', rarity='{self.rarity}')>"


class UserBadge(Base):
    """Badges earned by users."""

    __tablename__ = "user_badges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    badge_id: Mapped[int] = mapped_column(
        ForeignKey("badges.id", ondelete="CASCADE"),
        index=True
    )

    # Metadata
    earned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    notified: Mapped[bool] = mapped_column(default=False)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="badges")

    def __repr__(self) -> str:
        return f"<UserBadge(user_id={self.user_id}, badge_id={self.badge_id})>"


class DailyChallenge(Base):
    """Daily challenge definitions."""

    __tablename__ = "daily_challenges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Date
    challenge_date: Mapped[date] = mapped_column(Date, unique=True, index=True)

    # Challenge type
    challenge_type: Mapped[str] = mapped_column(String(50))  # lesson, puzzle, xp
    target_id: Mapped[Optional[int]] = mapped_column(Integer)  # specific lesson/puzzle
    target_count: Mapped[int] = mapped_column(Integer, default=1)

    # Reward
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)

    # Display
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"<DailyChallenge(date={self.challenge_date}, type='{self.challenge_type}')>"


class UserDailyChallenge(Base):
    """Track user completion of daily challenges."""

    __tablename__ = "user_daily_challenges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    challenge_id: Mapped[int] = mapped_column(
        ForeignKey("daily_challenges.id", ondelete="CASCADE"),
        index=True
    )

    # Progress
    progress: Mapped[int] = mapped_column(Integer, default=0)
    is_completed: Mapped[bool] = mapped_column(default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"<UserDailyChallenge(user_id={self.user_id}, challenge_id={self.challenge_id})>"
