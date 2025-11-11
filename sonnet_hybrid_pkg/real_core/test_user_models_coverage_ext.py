"""
Coverage Extension für src/user/models
Strategie: Model initialization, serialization, validation
Basiert auf Pydantic BaseModel (REVIDIERT)
"""

import pytest
from pydantic import ValidationError
from src.user.models import User, UserProfile, UserRole


class TestUserModelInit:
    """Test User model initialization"""
    
    def test_user_init_full(self):
        """Test creating User with all required fields"""
        user = User(
            id="user_1",
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        assert user.id == "user_1"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password_123"
    
    def test_user_init_minimal(self):
        """Test creating User with minimal required fields"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        # Defaults should be set
        assert user.role == UserRole.USER
        assert user.is_active is True
    
    def test_user_equality(self):
        """Test User equality comparison (excluding timestamps)"""
        user1 = User(
            id="1",
            username="test",
            email="test@test.com",
            password_hash="hash1"
        )
        user2 = User(
            id="1",
            username="test",
            email="test@test.com",
            password_hash="hash1"
        )
        # Compare key fields (timestamps may differ)
        assert user1.id == user2.id
        assert user1.username == user2.username
        assert user1.email == user2.email
        assert user1.password_hash == user2.password_hash
    
    def test_user_repr(self):
        """Test User string representation"""
        user = User(
            id="1",
            username="testuser",
            email="test@test.com",
            password_hash="hash"
        )
        repr_str = repr(user)
        assert "User" in repr_str or "testuser" in repr_str


class TestUserModelValidation:
    """Test User model validation"""
    
    def test_user_invalid_email(self):
        """Test User with invalid email format"""
        with pytest.raises(ValidationError):
            User(
                username="test",
                email="invalid-email",
                password_hash="hash"
            )
    
    def test_user_empty_username(self):
        """Test User with empty username"""
        with pytest.raises(ValidationError):
            User(
                username="",
                email="test@test.com",
                password_hash="hash"
            )
    
    def test_user_short_username(self):
        """Test User with username too short"""
        with pytest.raises(ValidationError):
            User(
                username="ab",  # Min 3 chars
                email="test@test.com",
                password_hash="hash"
            )
    
    def test_user_missing_password_hash(self):
        """Test User without required password_hash"""
        with pytest.raises(ValidationError):
            User(
                username="testuser",
                email="test@test.com"
            )
    
    def test_username_alphanumeric_validation(self):
        """Test username must be alphanumeric"""
        with pytest.raises(ValidationError):
            User(
                username="test@user",  # Special chars not allowed
                email="test@test.com",
                password_hash="hash"
            )


class TestUserModelSerialization:
    """Test User model serialization (Pydantic v1)"""
    
    def test_user_dict(self):
        """Test converting User to dictionary (Pydantic v1: dict())"""
        user = User(
            id="1",
            username="test",
            email="test@test.com",
            password_hash="hash"
        )
        data = user.dict()
        assert isinstance(data, dict)
        assert data['username'] == "test"
        assert data['email'] == "test@test.com"
    
    def test_user_json(self):
        """Test JSON serialization (Pydantic v1: json())"""
        user = User(
            id="1",
            username="test",
            email="test@test.com",
            password_hash="hash"
        )
        json_str = user.json()
        assert isinstance(json_str, str)
        assert "test" in json_str
    
    def test_user_parse_obj(self):
        """Test creating User from dict (Pydantic v1: parse_obj())"""
        data = {
            'id': '1',
            'username': 'test',
            'email': 'test@test.com',
            'password_hash': 'hash'
        }
        user = User.parse_obj(data)
        assert user.username == "test"


class TestUserProfileModel:
    """Test UserProfile model"""
    
    def test_profile_init(self):
        """Test creating UserProfile"""
        profile = UserProfile(
            user_id="user_123",
            display_name="Test User",
            bio="Test bio"
        )
        assert profile.user_id == "user_123"
        assert profile.display_name == "Test User"
        assert profile.bio == "Test bio"
    
    def test_profile_minimal(self):
        """Test UserProfile with minimal fields"""
        profile = UserProfile(user_id="user_123")
        assert profile.user_id == "user_123"
        assert profile.display_name is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
