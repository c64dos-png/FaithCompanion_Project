"""
User Module - Authentication, Profiles, and Preferences
FaithCompanion v1.2-FULL-HARDENED

This module handles:
- User authentication (registration, login, logout)
- User profiles and preferences
- Session management
- Password security
"""

from .models import User, UserProfile, UserPreferences
from .auth_service import AuthService
from .profile_service import ProfileService

__all__ = [
    "User",
    "UserProfile",
    "UserPreferences",
    "AuthService",
    "ProfileService",
]

__version__ = "1.0.0"
