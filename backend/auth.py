from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from functools import wraps
from flask import jsonify

def register_user(username, email, password):
    """Register a new user"""
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return {'error': 'Email already exists'}, 400
    
    if User.query.filter_by(username=username).first():
        return {'error': 'Username already exists'}, 400
    
    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return {'message': 'User registered successfully', 'user': user.to_dict()}, 201


def login_user(email, password):
    """Login user and return JWT token"""
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return {'error': 'Invalid email or password'}, 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return {
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }, 200


def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return {'error': 'Admin access required'}, 403
        
        return fn(*args, **kwargs)
    return wrapper
