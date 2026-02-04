"""
Authentication and session management for SmartChoice
"""

import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = "smartchoice_secret_key_2024"

def generate_token(user_id, email):
    """Generate JWT token for user authentication"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # 7 days expiry
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check token in header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Decode token
        data = decode_token(token)
        if not data:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        # Add user data to request
        request.current_user = {
            'user_id': data['user_id'],
            'email': data['email']
        }
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # For now, just check if user is authenticated
        # In production, check user role in database
        return token_required(f)(*args, **kwargs)
    
    return decorated
