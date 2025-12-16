# PromptCraft - Auth Endpoints

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.deps import DbSession, CurrentUser
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    verify_token_type
)
from app.models.user import User
from app.models.gamification import UserGamification
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordChangeRequest
)
from app.schemas.user import UserResponse
from app.config import settings

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: DbSession
) -> TokenResponse:
    """
    Register a new user account.

    Returns access and refresh tokens on successful registration.
    """
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Check if username already exists
    result = await db.execute(
        select(User).where(User.username == data.username.lower())
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    # Create user
    user = User(
        email=data.email,
        username=data.username.lower(),
        password_hash=get_password_hash(data.password),
        display_name=data.display_name or data.username,
        is_active=True,
        is_verified=False,  # TODO: Email verification
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(user)
    await db.flush()  # Get user.id

    # Create gamification record
    gamification = UserGamification(
        user_id=user.id,
        total_xp=0,
        level=1,
        current_streak=0,
        longest_streak=0,
        streak_freezes=2,  # Start with 2 streak freezes
        daily_xp_goal=50
    )
    db.add(gamification)
    await db.commit()

    # Generate tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: DbSession
) -> TokenResponse:
    """
    Authenticate user and return tokens.
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    user.last_activity = datetime.utcnow()
    await db.commit()

    # Generate tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    db: DbSession
) -> TokenResponse:
    """
    Refresh access token using refresh token.
    """
    # Verify refresh token
    payload = verify_token_type(data.refresh_token, "refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Verify user still exists and is active
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Generate new tokens
    access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CurrentUser
) -> UserResponse:
    """
    Get current authenticated user info.
    """
    return UserResponse.model_validate(current_user)


@router.post("/change-password")
async def change_password(
    data: PasswordChangeRequest,
    current_user: CurrentUser,
    db: DbSession
) -> dict:
    """
    Change current user's password.
    """
    # Verify current password
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    current_user.password_hash = get_password_hash(data.new_password)
    current_user.updated_at = datetime.utcnow()
    await db.commit()

    return {"message": "Password changed successfully"}


@router.post("/logout")
async def logout(
    current_user: CurrentUser
) -> dict:
    """
    Logout current user.

    Note: With JWT, logout is handled client-side by removing tokens.
    This endpoint can be used to invalidate tokens in Redis if needed.
    """
    # TODO: Add token to Redis blacklist if needed
    return {"message": "Logged out successfully"}
