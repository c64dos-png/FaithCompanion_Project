"""
Coverage Extension für src/user/profile_service
Strategie: Create-update-delete lifecycle, state persistence
Basiert auf echter Code-Struktur (REVIDIERT)
"""

import pytest
from src.user.profile_service import ProfileService


class TestProfileServiceLifecycle:
    """Test full lifecycle of profile operations"""
    
    def test_create_profile_with_display_name(self):
        """Test creating profile with display_name"""
        service = ProfileService()
        profile = service.create_profile(
            user_id="user_123",
            display_name="Test User"
        )
        assert profile is not None
        assert profile.user_id == "user_123"
        assert profile.display_name == "Test User"
    
    def test_create_profile_minimal(self):
        """Test creating profile with only user_id"""
        service = ProfileService()
        profile = service.create_profile(user_id="user_456")
        assert profile is not None
        assert profile.user_id == "user_456"
        assert profile.display_name is None
    
    def test_get_profile(self):
        """Test getting existing profile"""
        service = ProfileService()
        service.create_profile(user_id="user_123", display_name="Test")
        profile = service.get_profile(user_id="user_123")
        assert profile is not None
        assert profile.display_name == "Test"
    
    def test_update_profile(self):
        """Test updating profile"""
        service = ProfileService()
        service.create_profile(user_id="user_123", display_name="Original")
        updated = service.update_profile(user_id="user_123", display_name="Updated")
        assert updated is not None
        assert updated.display_name == "Updated"
    
    def test_update_profile_bio(self):
        """Test updating profile bio via kwargs"""
        service = ProfileService()
        service.create_profile(user_id="user_123")
        updated = service.update_profile(user_id="user_123", bio="New bio")
        assert updated is not None
        assert updated.bio == "New bio"
    
    def test_delete_profile(self):
        """Test profile deletion"""
        service = ProfileService()
        service.create_profile(user_id="user_123")
        result = service.delete_profile(user_id="user_123")
        assert result is True


class TestProfileServiceErrorHandling:
    """Test error handling"""
    
    def test_get_nonexistent_profile(self):
        """Test getting non-existent profile"""
        service = ProfileService()
        profile = service.get_profile(user_id="nonexistent")
        assert profile is None
    
    def test_update_nonexistent_profile(self):
        """Test updating profile that doesn't exist"""
        service = ProfileService()
        result = service.update_profile(user_id="nonexistent", display_name="Test")
        assert result is None
    
    def test_delete_nonexistent_profile(self):
        """Test deleting non-existent profile"""
        service = ProfileService()
        result = service.delete_profile(user_id="nonexistent")
        assert result is False


class TestProfileServicePreferences:
    """Test preferences operations"""
    
    def test_create_preferences(self):
        """Test creating default preferences"""
        service = ProfileService()
        prefs = service.create_preferences(user_id="user_123")
        assert prefs is not None
        assert prefs.user_id == "user_123"
        assert prefs.default_bible_version == "ESV"
    
    def test_get_preferences(self):
        """Test getting preferences"""
        service = ProfileService()
        service.create_preferences(user_id="user_123")
        prefs = service.get_preferences(user_id="user_123")
        assert prefs is not None
    
    def test_update_preferences(self):
        """Test updating preferences"""
        service = ProfileService()
        service.create_preferences(user_id="user_123")
        updated = service.update_preferences(
            user_id="user_123",
            default_bible_version="NIV",
            theme="dark"
        )
        assert updated is not None
        assert updated.default_bible_version == "NIV"
        assert updated.theme == "dark"
    
    def test_update_nonexistent_preferences(self):
        """Test updating non-existent preferences"""
        service = ProfileService()
        result = service.update_preferences(user_id="nonexistent", theme="dark")
        assert result is None
    
    def test_delete_preferences(self):
        """Test deleting preferences"""
        service = ProfileService()
        service.create_preferences(user_id="user_123")
        result = service.delete_preferences(user_id="user_123")
        assert result is True


class TestProfileServiceStatePersistence:
    """Test state persistence"""
    
    def test_profile_persists_after_create(self):
        """Test profile persists after creation"""
        service = ProfileService()
        service.create_profile(user_id="user_123", display_name="Test")
        profile = service.get_profile(user_id="user_123")
        assert profile is not None
        assert profile.display_name == "Test"
    
    def test_profile_updates_persist(self):
        """Test profile updates are persistent"""
        service = ProfileService()
        service.create_profile(user_id="user_123", display_name="Original")
        service.update_profile(user_id="user_123", display_name="Updated")
        profile = service.get_profile(user_id="user_123")
        assert profile.display_name == "Updated"
    
    def test_profile_not_found_after_delete(self):
        """Test profile is not retrievable after deletion"""
        service = ProfileService()
        service.create_profile(user_id="user_123")
        service.delete_profile(user_id="user_123")
        profile = service.get_profile(user_id="user_123")
        assert profile is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
