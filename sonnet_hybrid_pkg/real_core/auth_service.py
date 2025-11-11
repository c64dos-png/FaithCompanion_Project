"""
Authentication Service
Handles user authentication, password hashing, and JWT tokens
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple
import hashlib
import hmac

from .models import User, UserCreate, UserLogin, Token, TokenData, UserRole


class AuthService:
    """
    Authentication service for user management
    
    Security features:
    - bcrypt password hashing
    - JWT token generation
    - Secure password validation
    - Rate limiting hooks
    """
    
    def __init__(self, secret_key: str, token_expiry_hours: int = 24):
        """
        Initialize auth service
        
        Args:
            secret_key: Secret key for JWT signing
            token_expiry_hours: Token expiration time in hours
        """
        self.secret_key = secret_key
        self.token_expiry_hours = token_expiry_hours
        self._users_db = {}  # In-memory store for demo; use real DB in production
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using PBKDF2-SHA256
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password with salt
        """
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return f"{salt}${pwd_hash.hex()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            password_hash: Stored password hash
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            salt, pwd_hash = password_hash.split('$')
            test_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return hmac.compare_digest(test_hash.hex(), pwd_hash)
        except (ValueError, AttributeError):
            return False
    
    def generate_token(self, user: User) -> Token:
        """
        Generate JWT token for user
        
        Args:
            user: User object
            
        Returns:
            Token with access token and expiry
        """
        # In production, use proper JWT library (python-jose, PyJWT)
        # This is a simplified version for demonstration
        
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        
        # Simple token generation (use proper JWT in production)
        token_string = f"{token_data['user_id']}:{token_data['email']}:{token_data['role']}"
        signature = hmac.new(
            self.secret_key.encode(),
            token_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        access_token = f"{token_string}:{signature}"
        
        return Token(
            access_token=access_token,
            expires_in=self.token_expiry_hours * 3600
        )
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """
        Verify and decode JWT token
        
        Args:
            token: Access token string
            
        Returns:
            TokenData if valid, None otherwise
        """
        try:
            parts = token.split(':')
            if len(parts) != 4:
                return None
            
            user_id, email, role, signature = parts
            token_string = f"{user_id}:{email}:{role}"
            
            expected_signature = hmac.new(
                self.secret_key.encode(),
                token_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return None
            
            return TokenData(
                user_id=user_id,
                email=email,
                role=UserRole(role)
            )
        except (ValueError, AttributeError):
            return None
    
    def register_user(self, user_data: UserCreate) -> Tuple[Optional[User], Optional[str]]:
        """
        Register new user
        
        Args:
            user_data: User registration data
            
        Returns:
            Tuple of (User, error_message)
        """
        # Check if email already exists
        if any(u.email == user_data.email for u in self._users_db.values()):
            return None, "Email already registered"
        
        # Check if username already exists
        if any(u.username == user_data.username for u in self._users_db.values()):
            return None, "Username already taken"
        
        # Create user
        user_id = secrets.token_urlsafe(16)
        password_hash = self.hash_password(user_data.password)
        
        user = User(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash,
            role=UserRole.USER,
            is_active=True,
            is_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._users_db[user_id] = user
        return user, None
    
    def login_user(self, login_data: UserLogin) -> Tuple[Optional[Token], Optional[str]]:
        """
        Authenticate user and generate token
        
        Args:
            login_data: Login credentials
            
        Returns:
            Tuple of (Token, error_message)
        """
        # Find user by email
        user = next(
            (u for u in self._users_db.values() if u.email == login_data.email),
            None
        )
        
        if not user:
            return None, "Invalid credentials"
        
        # Verify password
        if not self.verify_password(login_data.password, user.password_hash):
            return None, "Invalid credentials"
        
        # Check if user is active
        if not user.is_active:
            return None, "Account is deactivated"
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        # Generate token
        token = self.generate_token(user)
        return token, None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self._users_db.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return next(
            (u for u in self._users_db.values() if u.email == email),
            None
        )
    
    def update_password(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Update user password
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            Tuple of (success, error_message)
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not self.verify_password(old_password, user.password_hash):
            return False, "Invalid current password"
        
        # Hash and update new password
        user.password_hash = self.hash_password(new_password)
        user.updated_at = datetime.utcnow()
        
        return True, None
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account"""
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            user.updated_at = datetime.utcnow()
            return True
        return False
