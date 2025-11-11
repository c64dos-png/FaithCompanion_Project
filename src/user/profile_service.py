"""
Profile Service
Manages user profiles and preferences
"""

from typing import Optional, Dict
from datetime import datetime

from .models import UserProfile, UserPreferences


class ProfileService:
    """Service for managing user profiles and preferences"""
    
    def __init__(self):
        """Initialize profile service"""
        self._profiles_db: Dict[str, UserProfile] = {}
        self._preferences_db: Dict[str, UserPreferences] = {}
    
    def create_profile(self, user_id: str, display_name: Optional[str] = None) -> UserProfile:
        """
        Create user profile
        
        Args:
            user_id: User ID
            display_name: Optional display name
            
        Returns:
            Created UserProfile
        """
        profile = UserProfile(
            user_id=user_id,
            display_name=display_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self._profiles_db[user_id] = profile
        return profile
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by user ID"""
        return self._profiles_db.get(user_id)
    
    def update_profile(self, user_id: str, **kwargs) -> Optional[UserProfile]:
        """
        Update user profile
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated UserProfile or None if not found
        """
        profile = self.get_profile(user_id)
        if not profile:
            return None
        
        for key, value in kwargs.items():
            if hasattr(profile, key) and key not in ['user_id', 'created_at']:
                setattr(profile, key, value)
        
        profile.updated_at = datetime.utcnow()
        return profile
    
    def create_preferences(self, user_id: str) -> UserPreferences:
        """
        Create default user preferences
        
        Args:
            user_id: User ID
            
        Returns:
            Created UserPreferences with defaults
        """
        preferences = UserPreferences(
            user_id=user_id,
            updated_at=datetime.utcnow()
        )
        self._preferences_db[user_id] = preferences
        return preferences
    
    def get_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences by user ID"""
        return self._preferences_db.get(user_id)
    
    def update_preferences(self, user_id: str, **kwargs) -> Optional[UserPreferences]:
        """
        Update user preferences
        
        Args:
            user_id: User ID
            **kwargs: Preference fields to update
            
        Returns:
            Updated UserPreferences or None if not found
        """
        preferences = self.get_preferences(user_id)
        if not preferences:
            return None
        
        for key, value in kwargs.items():
            if hasattr(preferences, key) and key not in ['user_id']:
                setattr(preferences, key, value)
        
        preferences.updated_at = datetime.utcnow()
        return preferences
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete user profile"""
        if user_id in self._profiles_db:
            del self._profiles_db[user_id]
            return True
        return False
    
    def delete_preferences(self, user_id: str) -> bool:
        """Delete user preferences"""
        if user_id in self._preferences_db:
            del self._preferences_db[user_id]
            return True
        return False
