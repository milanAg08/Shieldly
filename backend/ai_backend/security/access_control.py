# backend/ai_backend/security/access_control.py

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from ai_backend.models.user import User

class AccessControl:
    """Handles authentication and authorization"""
    
    @staticmethod
    def generate_token(user_id, expiration=24):
        """
        Generate a JWT token for a user
        
        Args:
            user_id (int): User ID
            expiration (int): Token expiration in hours
            
        Returns:
            str: JWT token
        """
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=expiration),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    
    @staticmethod
    def decode_token(token):
        """
        Decode a JWT token
        
        Args:
            token (str): JWT token
            
        Returns:
            dict: Token payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def token_required(f):
        """Decorator to require valid token for access to endpoints"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Check if token is in headers
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            # Decode token
            payload = AccessControl.decode_token(token)
            if not payload:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            # Get user from token
            user_id = payload['sub']
            current_user = User.query.get(user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            
            # Pass user to endpoint
            return f(current_user, *args, **kwargs)
        
        return decorated
    
    @staticmethod
    def is_age_appropriate(user, content_age_rating):
        """
        Check if content is age-appropriate for user
        
        Args:
            user (User): User object
            content_age_rating (int): Minimum age for content
            
        Returns:
            bool: True if content is appropriate for user's age
        """
        if not user.age:
            # If age is not provided, default to most restrictive
            return False
        
        return user.age >= content_age_rating