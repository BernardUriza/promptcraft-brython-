# PromptCraft - Puzzle Schemas

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from app.models.lesson import DifficultyLevel
from app.models.puzzle import PuzzleCategory


class PuzzleGridSize(BaseModel):
    """Puzzle grid size schema."""
    rows: int = Field(ge=2, le=6)
    cols: int = Field(ge=2, le=6)


class PuzzleClue(BaseModel):
    """Puzzle clue schema."""
    id: int
    text: str
    type: str = "positive"  # positive, negative, conditional


class PuzzleCategory_(BaseModel):
    """Puzzle category (column/row headers) schema."""
    name: str
    items: list[str]


class PuzzleBase(BaseModel):
    """Base puzzle schema."""
    slug: str
    title: str
    description: str
    icon: str = "🧩"
    category: PuzzleCategory
    difficulty: DifficultyLevel
    xp_reward: int = 50
    time_limit_seconds: Optional[int] = 300


class PuzzleResponse(PuzzleBase):
    """Full puzzle response schema."""
    id: int
    grid_size: PuzzleGridSize
    categories: list[PuzzleCategory_]
    clues: list[PuzzleClue]
    # Note: solution is NOT included in response
    is_daily: bool = False
    is_published: bool = True
    order: int = 0
    created_at: datetime
    updated_at: datetime

    # User-specific
    best_attempt: Optional["PuzzleAttemptResponse"] = None
    attempts_count: int = 0

    model_config = {"from_attributes": True}


class PuzzleListItem(BaseModel):
    """Puzzle list item (summary)."""
    id: int
    slug: str
    title: str
    description: str
    icon: str
    category: PuzzleCategory
    difficulty: DifficultyLevel
    xp_reward: int
    time_limit_seconds: Optional[int]
    order: int

    # User-specific
    is_completed: bool = False
    best_stars: int = 0
    attempts_count: int = 0

    model_config = {"from_attributes": True}


class PuzzleListResponse(BaseModel):
    """Paginated puzzle list response."""
    items: list[PuzzleListItem]
    total: int
    page: int
    per_page: int
    total_pages: int


class PuzzleAttemptCreate(BaseModel):
    """Create puzzle attempt schema."""
    puzzle_id: int


class PuzzleAttemptResponse(BaseModel):
    """Puzzle attempt response schema."""
    id: int
    puzzle_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    time_taken_seconds: Optional[int] = None
    is_completed: bool = False
    is_correct: bool = False
    stars: int = Field(ge=0, le=3)
    hints_used: int = 0
    xp_earned: int = 0

    model_config = {"from_attributes": True}


class PuzzleGridState(BaseModel):
    """Puzzle grid state for saving/resuming."""
    cells: dict[str, str]  # "row-col": "value" or "x" or ""
    last_updated: datetime


class PuzzleSubmit(BaseModel):
    """Submit puzzle solution schema."""
    attempt_id: int
    solution: dict[str, str]  # category item -> paired item
    time_taken_seconds: int = Field(ge=0)


class PuzzleResult(BaseModel):
    """Puzzle result schema."""
    is_correct: bool
    stars: int = Field(ge=0, le=3)
    xp_earned: int = 0
    time_taken_seconds: int
    time_bonus: int = 0
    hints_penalty: int = 0
    correct_pairs: int = 0
    total_pairs: int = 0
    feedback: str


class HintRequest(BaseModel):
    """Request hint for puzzle."""
    attempt_id: int


class HintResponse(BaseModel):
    """Hint response schema."""
    hint_number: int
    hint_text: str
    hints_remaining: int
    xp_penalty: int  # XP that will be deducted from final score
