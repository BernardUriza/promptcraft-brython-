# PromptCraft - User Model

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.gamification import UserGamification, UserBadge, XPTransaction
    from app.models.lesson import LessonProgress
    from app.models.puzzle import PuzzleAttempt


class User(Base):
    """User model for authentication and profile."""

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profile
    display_name: Mapped[Optional[str]] = mapped_column(String(100))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_activity: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Settings (JSON stored as text)
    settings: Mapped[Optional[str]] = mapped_column(Text)  # JSON string

    # Relationships
    gamification: Mapped["UserGamification"] = relationship(
        "UserGamification",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    badges: Mapped[List["UserBadge"]] = relationship(
        "UserBadge",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    xp_transactions: Mapped[List["XPTransaction"]] = relationship(
        "XPTransaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    lesson_progress: Mapped[List["LessonProgress"]] = relationship(
        "LessonProgress",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    puzzle_attempts: Mapped[List["PuzzleAttempt"]] = relationship(
        "PuzzleAttempt",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
