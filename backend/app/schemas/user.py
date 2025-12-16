# PromptCraft - User Schemas

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserSettings(BaseModel):
    """User settings schema."""
    theme: str = "light"
    daily_goal: int = Field(default=50, ge=10, le=500)
    notifications_enabled: bool = True
    sound_enabled: bool = True
    language: str = "es"


class UserBase(BaseModel):
    """Base user schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    display_name: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, underscores, and hyphens"
            )
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for user profile update."""
    display_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = Field(None, max_length=500)
    settings: Optional[UserSettings] = None


class UserResponse(BaseModel):
    """Full user response schema (for authenticated user)."""
    id: int
    email: EmailStr
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    settings: Optional[UserSettings] = None

    model_config = {"from_attributes": True}


class UserPublic(BaseModel):
    """Public user profile (visible to others)."""
    id: int
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

    # Gamification stats (public)
    level: int = 1
    total_xp: int = 0
    current_streak: int = 0
    lessons_completed: int = 0
    puzzles_completed: int = 0

    model_config = {"from_attributes": True}


class UserWithGamification(UserResponse):
    """User response with gamification stats."""
    level: int = 1
    total_xp: int = 0
    xp_to_next_level: int = 100
    current_streak: int = 0
    longest_streak: int = 0
    lessons_completed: int = 0
    puzzles_completed: int = 0
    badges_earned: int = 0
    daily_xp_earned: int = 0
    daily_xp_goal: int = 50
