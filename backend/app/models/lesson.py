# PromptCraft - Lesson Models

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User


class DifficultyLevel(str, enum.Enum):
    """Difficulty levels for lessons and puzzles."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LessonCategory(str, enum.Enum):
    """Categories for lessons."""
    FUNDAMENTALS = "fundamentals"
    TECHNIQUES = "techniques"
    ADVANCED = "advanced"
    APPLICATIONS = "applications"


class ProgressStatus(str, enum.Enum):
    """Progress status for lessons."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Lesson(Base):
    """Lesson content model."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Identification
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    # Content
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(10), default="📚")

    # Classification
    category: Mapped[LessonCategory] = mapped_column(
        Enum(LessonCategory),
        default=LessonCategory.FUNDAMENTALS
    )
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel),
        default=DifficultyLevel.BEGINNER
    )

    # Metadata
    duration_minutes: Mapped[int] = mapped_column(Integer, default=10)
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Content (JSON stored as text)
    content: Mapped[str] = mapped_column(Text)  # JSON with sections
    objectives: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    exercise: Mapped[Optional[str]] = mapped_column(Text)  # JSON

    # Navigation
    next_lesson_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=True
    )

    # Status
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
        return f"<Lesson(id={self.id}, title='{self.title}')>"


class LessonProgress(Base):
    """Track user progress through lessons."""

    __tablename__ = "lesson_progress"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        index=True
    )

    # Progress
    status: Mapped[ProgressStatus] = mapped_column(
        Enum(ProgressStatus),
        default=ProgressStatus.NOT_STARTED
    )
    current_section: Mapped[int] = mapped_column(Integer, default=0)
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)

    # Exercise
    exercise_completed: Mapped[bool] = mapped_column(default=False)
    exercise_answer: Mapped[Optional[str]] = mapped_column(Text)
    exercise_score: Mapped[Optional[int]] = mapped_column(Integer)

    # Timestamps
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_accessed: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="lesson_progress")

    def __repr__(self) -> str:
        return f"<LessonProgress(user_id={self.user_id}, lesson_id={self.lesson_id}, status='{self.status}')>"
