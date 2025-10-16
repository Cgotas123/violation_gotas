"""
auth.py - Authentication module for Vehicle Violation System
"""
import hashlib
from database import ViolationDatabase

class AuthManager:
    def __init__(self, db):
        self.db = db
        
    def register_user(self, username, email, password, role='officer'):
        """Register a new user with hashed password"""
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return self.db.create_user(username, email, hashed, role)
        
    def login_user(self, username, password):
        """Authenticate user"""
        user = self.db.get_user_by_username(username)
        if user and user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
            return user
        return None
        
    def user_exists(self, username):
        """Check if username exists"""
        return bool(self.db.get_user_by_username(username))
