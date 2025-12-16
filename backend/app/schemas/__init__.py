# PromptCraft - Pydantic Schemas
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserPublic,
    UserSettings
)
from app.schemas.auth import (
    TokenResponse,
    TokenPayload,
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    PasswordChangeRequest
)
from app.schemas.lesson import (
    LessonResponse,
    LessonListResponse,
    LessonProgressResponse,
    LessonProgressUpdate,
    ExerciseSubmit
)
from app.schemas.puzzle import (
    PuzzleResponse,
    PuzzleListResponse,
    PuzzleAttemptCreate,
    PuzzleAttemptResponse,
    PuzzleSubmit
)
from app.schemas.gamification import (
    GamificationStatsResponse,
    XPTransactionResponse,
    BadgeResponse,
    UserBadgeResponse,
    LeaderboardEntry,
    LeaderboardResponse,
    DailyChallengeResponse,
    StreakResponse
)

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserPublic",
    "UserSettings",
    # Auth
    "TokenResponse",
    "TokenPayload",
    "LoginRequest",
    "RegisterRequest",
    "RefreshTokenRequest",
    "PasswordChangeRequest",
    # Lesson
    "LessonResponse",
    "LessonListResponse",
    "LessonProgressResponse",
    "LessonProgressUpdate",
    "ExerciseSubmit",
    # Puzzle
    "PuzzleResponse",
    "PuzzleListResponse",
    "PuzzleAttemptCreate",
    "PuzzleAttemptResponse",
    "PuzzleSubmit",
    # Gamification
    "GamificationStatsResponse",
    "XPTransactionResponse",
    "BadgeResponse",
    "UserBadgeResponse",
    "LeaderboardEntry",
    "LeaderboardResponse",
    "DailyChallengeResponse",
    "StreakResponse"
]
