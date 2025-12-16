# PromptCraft - Users Endpoints

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.deps import DbSession, CurrentUser, OptionalUser
from app.models.user import User
from app.models.gamification import UserGamification, UserBadge
from app.schemas.user import UserResponse, UserUpdate, UserPublic

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: CurrentUser
) -> UserResponse:
    """
    Get current user's full profile.
    """
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdate,
    current_user: CurrentUser,
    db: DbSession
) -> UserResponse:
    """
    Update current user's profile.
    """
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "settings" and value is not None:
            # Convert settings to JSON string
            import json
            setattr(current_user, field, json.dumps(value.model_dump()))
        else:
            setattr(current_user, field, value)

    current_user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(current_user)

    return UserResponse.model_validate(current_user)


@router.get("/{username}", response_model=UserPublic)
async def get_user_profile(
    username: str,
    db: DbSession,
    current_user: OptionalUser = None
) -> UserPublic:
    """
    Get public profile of a user by username.
    """
    result = await db.execute(
        select(User)
        .options(selectinload(User.gamification))
        .where(User.username == username.lower())
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Build public profile with gamification stats
    gamification = user.gamification
    return UserPublic(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        created_at=user.created_at,
        level=gamification.level if gamification else 1,
        total_xp=gamification.total_xp if gamification else 0,
        current_streak=gamification.current_streak if gamification else 0,
        lessons_completed=gamification.lessons_completed if gamification else 0,
        puzzles_completed=gamification.puzzles_completed if gamification else 0
    )


@router.get("/", response_model=list[UserPublic])
async def search_users(
    db: DbSession,
    q: str = Query(None, min_length=2, description="Search query"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
) -> list[UserPublic]:
    """
    Search users by username or display name.
    """
    query = (
        select(User)
        .options(selectinload(User.gamification))
        .where(User.is_active == True)
    )

    if q:
        search_term = f"%{q.lower()}%"
        query = query.where(
            (User.username.ilike(search_term)) |
            (User.display_name.ilike(search_term))
        )

    # Order by XP (most active users first)
    query = (
        query
        .join(UserGamification)
        .order_by(UserGamification.total_xp.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    result = await db.execute(query)
    users = result.scalars().all()

    return [
        UserPublic(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            bio=user.bio,
            created_at=user.created_at,
            level=user.gamification.level if user.gamification else 1,
            total_xp=user.gamification.total_xp if user.gamification else 0,
            current_streak=user.gamification.current_streak if user.gamification else 0,
            lessons_completed=user.gamification.lessons_completed if user.gamification else 0,
            puzzles_completed=user.gamification.puzzles_completed if user.gamification else 0
        )
        for user in users
    ]


@router.delete("/me")
async def delete_my_account(
    current_user: CurrentUser,
    db: DbSession
) -> dict:
    """
    Delete current user's account.
    """
    await db.delete(current_user)
    await db.commit()

    return {"message": "Account deleted successfully"}
