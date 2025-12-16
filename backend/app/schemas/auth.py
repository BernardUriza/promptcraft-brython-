# PromptCraft - Auth Schemas

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str = Field(min_length=1)
    remember_me: bool = False


class RegisterRequest(BaseModel):
    """Registration request schema."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expires


class TokenPayload(BaseModel):
    """JWT token payload schema."""
    sub: str  # user_id
    exp: datetime
    iat: datetime
    type: str  # 'access' or 'refresh'


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Password change request schema."""
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=100)


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str
    new_password: str = Field(min_length=8, max_length=100)


class EmailVerificationRequest(BaseModel):
    """Email verification request schema."""
    token: str
