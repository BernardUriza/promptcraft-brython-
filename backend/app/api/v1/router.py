# PromptCraft - API v1 Router

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, lessons, puzzles, gamification, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    lessons.router,
    prefix="/lessons",
    tags=["Lessons"]
)

api_router.include_router(
    puzzles.router,
    prefix="/puzzles",
    tags=["Puzzles"]
)

api_router.include_router(
    gamification.router,
    prefix="/gamification",
    tags=["Gamification"]
)

# WebSocket endpoint (no prefix, handled at /api/v1/ws)
api_router.include_router(
    websocket.router,
    tags=["WebSocket"]
)
