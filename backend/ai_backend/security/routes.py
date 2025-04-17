# backend/ai_backend/security/routes.py

from flask import Blueprint, request, jsonify
from ai_backend.security.data_encryption import DataEncryption
from ai_backend.security.access_control import AccessControl
from ai_backend.models.user import User
from extensions import db

security_bp = Blueprint('security', __name__)

# Initialize encryption
encryptor = DataEncryption()

@security_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or 'username' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409
    
    # Create new user
    new_user = User(
        username=data['username'],
        age=data.get('age'),
        language_preference=data.get('language_preference', 'en')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate token for new user
    token = AccessControl.generate_token(new_user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': new_user.id,
        'token': token
    }), 201

@security_bp.route('/login', methods=['POST'])
def login():
    """Login an existing user"""
    data = request.get_json()
    
    if not data or 'username' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # In a real application, you would verify password here
    # For this demo, we're just checking username
    
    # Generate token
    token = AccessControl.generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user_id': user.id,
        'token': token
    })

@security_bp.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypt sensitive data"""
    data = request.get_json()
    
    if not data or 'data' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Encrypt data
    encrypted_data = encryptor.encrypt(data['data'])
    
    return jsonify({'encrypted_data': encrypted_data})

@security_bp.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypt encrypted data"""
    data = request.get_json()
    
    if not data or 'encrypted_data' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Decrypt data
    decrypted_data = encryptor.decrypt(data['encrypted_data'])
    
    if decrypted_data is None:
        return jsonify({'error': 'Failed to decrypt data'}), 400
    
    return jsonify({'decrypted_data': decrypted_data})

@security_bp.route('/check-token', methods=['GET'])
@AccessControl.token_required
def check_token(current_user):
    """Check if token is valid"""
    return jsonify({
        'message': 'Token is valid',
        'user_id': current_user.id,
        'username': current_user.username
    })