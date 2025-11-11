"""
Tests for Authentication Service
Comprehensive test coverage for user authentication
"""

import pytest
from datetime import datetime

from src.user.auth_service import AuthService
from src.user.models import UserCreate, UserLogin, UserRole


@pytest.fixture
def auth_service():
    """Create auth service instance"""
    return AuthService(secret_key="test_secret_key_do_not_use_in_production", token_expiry_hours=24)


@pytest.fixture
def sample_user_data():
    """Sample user registration data"""
    return UserCreate(
        email="test@example.com",
        username="testuser",
        password="TestPass123"
    )


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password_creates_hash(self, auth_service):
        """Test that password hashing creates a hash"""
        password = "TestPassword123"
        hashed = auth_service.hash_password(password)
        
        assert hashed is not None
        assert '$' in hashed  # Salt separator
        assert hashed != password
    
    def test_hash_password_is_unique(self, auth_service):
        """Test that same password creates different hashes (due to salt)"""
        password = "TestPassword123"
        hash1 = auth_service.hash_password(password)
        hash2 = auth_service.hash_password(password)
        
        assert hash1 != hash2
    
    def test_verify_password_correct(self, auth_service):
        """Test password verification with correct password"""
        password = "TestPassword123"
        hashed = auth_service.hash_password(password)
        
        assert auth_service.verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self, auth_service):
        """Test password verification with incorrect password"""
        password = "TestPassword123"
        hashed = auth_service.hash_password(password)
        
        assert auth_service.verify_password("WrongPassword", hashed) is False
    
    def test_verify_password_invalid_hash(self, auth_service):
        """Test password verification with malformed hash"""
        assert auth_service.verify_password("password", "invalid_hash") is False


class TestUserRegistration:
    """Test user registration"""
    
    def test_register_user_success(self, auth_service, sample_user_data):
        """Test successful user registration"""
        user, error = auth_service.register_user(sample_user_data)
        
        assert user is not None
        assert error is None
        assert user.email == sample_user_data.email
        assert user.username == sample_user_data.username
        assert user.id is not None
        assert user.role == UserRole.USER
        assert user.is_active is True
        assert user.is_verified is False
    
    def test_register_user_duplicate_email(self, auth_service, sample_user_data):
        """Test registration with duplicate email"""
        # Register first user
        auth_service.register_user(sample_user_data)
        
        # Try to register again with same email
        user, error = auth_service.register_user(sample_user_data)
        
        assert user is None
        assert error == "Email already registered"
    
    def test_register_user_duplicate_username(self, auth_service):
        """Test registration with duplicate username"""
        # Register first user
        user_data1 = UserCreate(
            email="user1@example.com",
            username="testuser",
            password="TestPass123"
        )
        auth_service.register_user(user_data1)
        
        # Try with same username but different email
        user_data2 = UserCreate(
            email="user2@example.com",
            username="testuser",
            password="TestPass123"
        )
        user, error = auth_service.register_user(user_data2)
        
        assert user is None
        assert error == "Username already taken"
    
    def test_register_user_password_hashed(self, auth_service, sample_user_data):
        """Test that password is hashed during registration"""
        user, error = auth_service.register_user(sample_user_data)
        
        assert user.password_hash != sample_user_data.password
        assert auth_service.verify_password(sample_user_data.password, user.password_hash)


class TestUserLogin:
    """Test user login"""
    
    def test_login_success(self, auth_service, sample_user_data):
        """Test successful login"""
        # Register user first
        auth_service.register_user(sample_user_data)
        
        # Login
        login_data = UserLogin(
            email=sample_user_data.email,
            password=sample_user_data.password
        )
        token, error = auth_service.login_user(login_data)
        
        assert token is not None
        assert error is None
        assert token.access_token is not None
        assert token.token_type == "bearer"
        assert token.expires_in == 24 * 3600
    
    def test_login_invalid_email(self, auth_service):
        """Test login with non-existent email"""
        login_data = UserLogin(
            email="nonexistent@example.com",
            password="TestPass123"
        )
        token, error = auth_service.login_user(login_data)
        
        assert token is None
        assert error == "Invalid credentials"
    
    def test_login_invalid_password(self, auth_service, sample_user_data):
        """Test login with wrong password"""
        # Register user first
        auth_service.register_user(sample_user_data)
        
        # Login with wrong password
        login_data = UserLogin(
            email=sample_user_data.email,
            password="WrongPassword123"
        )
        token, error = auth_service.login_user(login_data)
        
        assert token is None
        assert error == "Invalid credentials"
    
    def test_login_inactive_user(self, auth_service, sample_user_data):
        """Test login with deactivated account"""
        # Register and deactivate user
        user, _ = auth_service.register_user(sample_user_data)
        auth_service.deactivate_user(user.id)
        
        # Try to login
        login_data = UserLogin(
            email=sample_user_data.email,
            password=sample_user_data.password
        )
        token, error = auth_service.login_user(login_data)
        
        assert token is None
        assert error == "Account is deactivated"


class TestTokenGeneration:
    """Test JWT token generation and verification"""
    
    def test_generate_token(self, auth_service, sample_user_data):
        """Test token generation"""
        user, _ = auth_service.register_user(sample_user_data)
        token = auth_service.generate_token(user)
        
        assert token.access_token is not None
        assert ':' in token.access_token  # Contains user data
    
    def test_verify_token_valid(self, auth_service, sample_user_data):
        """Test verification of valid token"""
        user, _ = auth_service.register_user(sample_user_data)
        token = auth_service.generate_token(user)
        
        token_data = auth_service.verify_token(token.access_token)
        
        assert token_data is not None
        assert token_data.user_id == user.id
        assert token_data.email == user.email
        assert token_data.role == user.role
    
    def test_verify_token_invalid(self, auth_service):
        """Test verification of invalid token"""
        token_data = auth_service.verify_token("invalid_token")
        assert token_data is None
    
    def test_verify_token_tampered(self, auth_service, sample_user_data):
        """Test verification of tampered token"""
        user, _ = auth_service.register_user(sample_user_data)
        token = auth_service.generate_token(user)
        
        # Tamper with token
        tampered_token = token.access_token[:-5] + "xxxxx"
        token_data = auth_service.verify_token(tampered_token)
        
        assert token_data is None


class TestUserRetrieval:
    """Test user retrieval methods"""
    
    def test_get_user_by_id(self, auth_service, sample_user_data):
        """Test getting user by ID"""
        user, _ = auth_service.register_user(sample_user_data)
        retrieved = auth_service.get_user_by_id(user.id)
        
        assert retrieved is not None
        assert retrieved.id == user.id
        assert retrieved.email == user.email
    
    def test_get_user_by_email(self, auth_service, sample_user_data):
        """Test getting user by email"""
        user, _ = auth_service.register_user(sample_user_data)
        retrieved = auth_service.get_user_by_email(user.email)
        
        assert retrieved is not None
        assert retrieved.email == user.email
        assert retrieved.id == user.id
    
    def test_get_user_not_found(self, auth_service):
        """Test getting non-existent user"""
        assert auth_service.get_user_by_id("nonexistent") is None
        assert auth_service.get_user_by_email("none@example.com") is None


class TestPasswordUpdate:
    """Test password update functionality"""
    
    def test_update_password_success(self, auth_service, sample_user_data):
        """Test successful password update"""
        user, _ = auth_service.register_user(sample_user_data)
        
        success, error = auth_service.update_password(
            user.id,
            sample_user_data.password,
            "NewPassword123"
        )
        
        assert success is True
        assert error is None
        
        # Verify new password works
        user = auth_service.get_user_by_id(user.id)
        assert auth_service.verify_password("NewPassword123", user.password_hash)
    
    def test_update_password_wrong_old(self, auth_service, sample_user_data):
        """Test password update with wrong old password"""
        user, _ = auth_service.register_user(sample_user_data)
        
        success, error = auth_service.update_password(
            user.id,
            "WrongOldPassword",
            "NewPassword123"
        )
        
        assert success is False
        assert error == "Invalid current password"
    
    def test_update_password_user_not_found(self, auth_service):
        """Test password update for non-existent user"""
        success, error = auth_service.update_password(
            "nonexistent",
            "OldPass123",
            "NewPass123"
        )
        
        assert success is False
        assert error == "User not found"


class TestUserDeactivation:
    """Test user account deactivation"""
    
    def test_deactivate_user_success(self, auth_service, sample_user_data):
        """Test successful user deactivation"""
        user, _ = auth_service.register_user(sample_user_data)
        
        result = auth_service.deactivate_user(user.id)
        assert result is True
        
        # Verify user is inactive
        user = auth_service.get_user_by_id(user.id)
        assert user.is_active is False
    
    def test_deactivate_user_not_found(self, auth_service):
        """Test deactivating non-existent user"""
        result = auth_service.deactivate_user("nonexistent")
        assert result is False
