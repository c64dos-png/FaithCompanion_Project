"""
User Models
Data models for user, profile, and preferences
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(BaseModel):
    """Core user model"""
    id: Optional[str] = None
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password_hash: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    @validator('username', allow_reuse=True)
    def username_alphanumeric(cls, v):
        """Ensure username is alphanumeric with underscores"""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "faithful_user",
                "role": "user",
                "is_active": True
            }
        }


class UserProfile(BaseModel):
    """User profile with personal information"""
    user_id: str
    display_name: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "display_name": "John Faithful",
                "bio": "Seeking God daily through His Word"
            }
        }


class UserPreferences(BaseModel):
    """User preferences and settings"""
    user_id: str
    default_bible_version: str = "ESV"
    reading_plan_active: bool = False
    daily_reminder_enabled: bool = True
    reminder_time: Optional[str] = "08:00"  # HH:MM format
    font_size: int = Field(default=16, ge=12, le=24)
    theme: str = Field(default="light", pattern="^(light|dark|auto)$")
    language: str = "en"
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('reminder_time')
    def validate_time_format(cls, v):
        """Validate HH:MM time format"""
        if v is not None:
            try:
                hour, minute = v.split(':')
                if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                    raise ValueError
            except (ValueError, AttributeError):
                raise ValueError('Time must be in HH:MM format (00:00-23:59)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "default_bible_version": "NIV",
                "daily_reminder_enabled": True,
                "reminder_time": "07:30",
                "theme": "dark"
            }
        }


class UserCreate(BaseModel):
    """Model for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v


class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Data encoded in JWT token"""
    user_id: str
    email: str
    role: UserRole
