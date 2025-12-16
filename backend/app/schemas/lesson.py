# PromptCraft - Lesson Schemas

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from app.models.lesson import DifficultyLevel, LessonCategory, ProgressStatus


class LessonSection(BaseModel):
    """Lesson section schema."""
    type: str  # text, code, exercise, quiz, tip
    title: Optional[str] = None
    content: str
    language: Optional[str] = None  # for code blocks
    options: Optional[list[str]] = None  # for quiz
    correct_answer: Optional[int] = None  # for quiz


class LessonExercise(BaseModel):
    """Lesson exercise schema."""
    type: str  # prompt_writing, multiple_choice, fill_blank
    instruction: str
    template: Optional[str] = None
    options: Optional[list[str]] = None
    correct_answer: Optional[str | int] = None
    hints: list[str] = []


class LessonBase(BaseModel):
    """Base lesson schema."""
    slug: str
    title: str
    description: str
    icon: str = "📚"
    category: LessonCategory
    difficulty: DifficultyLevel
    duration_minutes: int = 10
    xp_reward: int = 50


class LessonResponse(LessonBase):
    """Full lesson response schema."""
    id: int
    content: list[LessonSection]
    objectives: list[str] = []
    exercise: Optional[LessonExercise] = None
    next_lesson_id: Optional[int] = None
    is_published: bool = True
    order: int = 0
    created_at: datetime
    updated_at: datetime

    # User-specific (if authenticated)
    user_progress: Optional["LessonProgressResponse"] = None

    model_config = {"from_attributes": True}


class LessonListItem(BaseModel):
    """Lesson list item (summary)."""
    id: int
    slug: str
    title: str
    description: str
    icon: str
    category: LessonCategory
    difficulty: DifficultyLevel
    duration_minutes: int
    xp_reward: int
    order: int

    # User-specific
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    progress_percent: int = 0

    model_config = {"from_attributes": True}


class LessonListResponse(BaseModel):
    """Paginated lesson list response."""
    items: list[LessonListItem]
    total: int
    page: int
    per_page: int
    total_pages: int


class LessonProgressResponse(BaseModel):
    """Lesson progress response schema."""
    lesson_id: int
    status: ProgressStatus
    current_section: int
    progress_percent: int
    exercise_completed: bool
    exercise_score: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed: datetime

    model_config = {"from_attributes": True}


class LessonProgressUpdate(BaseModel):
    """Update lesson progress schema."""
    current_section: Optional[int] = Field(None, ge=0)
    progress_percent: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[ProgressStatus] = None


class ExerciseSubmit(BaseModel):
    """Submit lesson exercise schema."""
    answer: str | int | list[str]


class ExerciseResult(BaseModel):
    """Exercise result schema."""
    is_correct: bool
    score: int = Field(ge=0, le=100)
    feedback: str
    xp_earned: int = 0
    correct_answer: Optional[str | int] = None
