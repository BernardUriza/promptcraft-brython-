# PromptCraft - Puzzle Models

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base
from app.models.lesson import DifficultyLevel

if TYPE_CHECKING:
    from app.models.user import User


class PuzzleCategory(str, enum.Enum):
    """Categories for puzzles."""
    FUNDAMENTALS = "fundamentals"
    TECHNIQUES = "techniques"
    ADVANCED = "advanced"
    APPLICATIONS = "applications"


class Puzzle(Base):
    """Logic Grid Puzzle model."""

    __tablename__ = "puzzles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Identification
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Content
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(10), default="🧩")

    # Classification
    category: Mapped[PuzzleCategory] = mapped_column(
        Enum(PuzzleCategory),
        default=PuzzleCategory.FUNDAMENTALS
    )
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel),
        default=DifficultyLevel.BEGINNER
    )

    # Puzzle data (JSON)
    grid_size: Mapped[str] = mapped_column(Text)  # JSON: {"rows": 4, "cols": 4}
    categories: Mapped[str] = mapped_column(Text)  # JSON array of categories
    clues: Mapped[str] = mapped_column(Text)  # JSON array of clues
    solution: Mapped[str] = mapped_column(Text)  # JSON solution mapping

    # Rewards
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    time_limit_seconds: Mapped[Optional[int]] = mapped_column(Integer, default=300)

    # Metadata
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_daily: Mapped[bool] = mapped_column(default=False)
    is_published: Mapped[bool] = mapped_column(default=True)

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

    def __repr__(self) -> str:
        return f"<Puzzle(id={self.id}, title='{self.title}')>"


class PuzzleAttempt(Base):
    """Track user attempts at puzzles."""

    __tablename__ = "puzzle_attempts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    puzzle_id: Mapped[int] = mapped_column(
        ForeignKey("puzzles.id", ondelete="CASCADE"),
        index=True
    )

    # Attempt data
    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(Integer)

    # Result
    is_completed: Mapped[bool] = mapped_column(default=False)
    is_correct: Mapped[bool] = mapped_column(default=False)
    stars: Mapped[int] = mapped_column(Integer, default=0)  # 0-3 stars
    hints_used: Mapped[int] = mapped_column(Integer, default=0)

    # XP earned
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)

    # Grid state (JSON) - for resuming
    grid_state: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="puzzle_attempts")

    def __repr__(self) -> str:
        return f"<PuzzleAttempt(user_id={self.user_id}, puzzle_id={self.puzzle_id}, stars={self.stars})>"
