"""
Tests for Profile Service
Test coverage for user profiles and preferences
"""

import pytest
from src.user.profile_service import ProfileService


@pytest.fixture
def profile_service():
    """Create profile service instance"""
    return ProfileService()


class TestProfileManagement:
    """Test profile creation and management"""
    
    def test_create_profile(self, profile_service):
        """Test profile creation"""
        profile = profile_service.create_profile("user_123", "Test User")
        
        assert profile is not None
        assert profile.user_id == "user_123"
        assert profile.display_name == "Test User"
    
    def test_get_profile(self, profile_service):
        """Test getting profile"""
        profile_service.create_profile("user_123")
        profile = profile_service.get_profile("user_123")
        
        assert profile is not None
        assert profile.user_id == "user_123"
    
    def test_update_profile(self, profile_service):
        """Test profile update"""
        profile_service.create_profile("user_123")
        updated = profile_service.update_profile(
            "user_123",
            display_name="Updated Name",
            bio="New bio"
        )
        
        assert updated.display_name == "Updated Name"
        assert updated.bio == "New bio"
    
    def test_delete_profile(self, profile_service):
        """Test profile deletion"""
        profile_service.create_profile("user_123")
        result = profile_service.delete_profile("user_123")
        
        assert result is True
        assert profile_service.get_profile("user_123") is None


class TestPreferencesManagement:
    """Test user preferences"""
    
    def test_create_preferences(self, profile_service):
        """Test preferences creation with defaults"""
        prefs = profile_service.create_preferences("user_123")
        
        assert prefs.user_id == "user_123"
        assert prefs.default_bible_version == "ESV"
        assert prefs.font_size == 16
        assert prefs.theme == "light"
    
    def test_get_preferences(self, profile_service):
        """Test getting preferences"""
        profile_service.create_preferences("user_123")
        prefs = profile_service.get_preferences("user_123")
        
        assert prefs is not None
        assert prefs.user_id == "user_123"
    
    def test_update_preferences(self, profile_service):
        """Test preferences update"""
        profile_service.create_preferences("user_123")
        updated = profile_service.update_preferences(
            "user_123",
            default_bible_version="NIV",
            theme="dark",
            font_size=18
        )
        
        assert updated.default_bible_version == "NIV"
        assert updated.theme == "dark"
        assert updated.font_size == 18
    
    def test_delete_preferences(self, profile_service):
        """Test preferences deletion"""
        profile_service.create_preferences("user_123")
        result = profile_service.delete_preferences("user_123")
        
        assert result is True
        assert profile_service.get_preferences("user_123") is None
