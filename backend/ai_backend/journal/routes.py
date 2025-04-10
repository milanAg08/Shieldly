# backend/ai_backend/journal/routes.py

from flask import Blueprint, request, jsonify
from extensions import db
from ai_backend.models.journal import JournalEntry
from ai_backend.models.user import User
from ai_backend.security.access_control import AccessControl
from ai_backend.security.data_encryption import DataEncryption

journal_bp = Blueprint('journal', __name__)
encryptor = DataEncryption()

@journal_bp.route('/entries', methods=['POST'])
@AccessControl.token_required
def create_entry(current_user):
    """Create a new journal entry"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check if entry should be encrypted
    is_sensitive = data.get('is_sensitive', False)
    content = data['content']
    encrypted_content = None
    
    if is_sensitive:
        # Encrypt content
        encrypted_content = encryptor.encrypt(content)
    
    # Create new journal entry
    new_entry = JournalEntry(
        user_id=current_user.id,
        mood=data.get('mood'),
        content=content if not is_sensitive else None,
        is_sensitive=is_sensitive,
        encrypted_content=encrypted_content
    )
    
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Journal entry created successfully',
        'entry_id': new_entry.id
    }), 201

@journal_bp.route('/entries', methods=['GET'])
@AccessControl.token_required
def get_entries(current_user):
    """Get all journal entries for current user"""
    entries = JournalEntry.query.filter_by(user_id=current_user.id).all()
    
    result = []
    for entry in entries:
        entry_data = {
            'id': entry.id,
            'date': entry.entry_date.isoformat(),
            'mood': entry.mood
        }
        
        if entry.is_sensitive:
            # Decrypt content
            if entry.encrypted_content:
                entry_data['content'] = encryptor.decrypt(entry.encrypted_content)
            else:
                entry_data['content'] = '[Encrypted content not available]'
        else:
            entry_data['content'] = entry.content
        
        result.append(entry_data)
    
    return jsonify(result)

@journal_bp.route('/entries/<int:entry_id>', methods=['GET'])
@AccessControl.token_required
def get_entry(current_user, entry_id):
    """Get a specific journal entry"""
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    entry_data = {
        'id': entry.id,
        'date': entry.entry_date.isoformat(),
        'mood': entry.mood
    }
    
    if entry.is_sensitive:
        # Decrypt content
        if entry.encrypted_content:
            entry_data['content'] = encryptor.decrypt(entry.encrypted_content)
        else:
            entry_data['content'] = '[Encrypted content not available]'
    else:
        entry_data['content'] = entry.content
    
    return jsonify(entry_data)

@journal_bp.route('/entries/<int:entry_id>', methods=['PUT'])
@AccessControl.token_required
def update_entry(current_user, entry_id):
    """Update a journal entry"""
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'mood' in data:
        entry.mood = data['mood']
    
    if 'content' in data:
        is_sensitive = data.get('is_sensitive', entry.is_sensitive)
        
        if is_sensitive:
            # Encrypt content
            entry.encrypted_content = encryptor.encrypt(data['content'])
            entry.content = None
        else:
            entry.content = data['content']
            entry.encrypted_content = None
        
        entry.is_sensitive = is_sensitive
    
    db.session.commit()
    
    return jsonify({'message': 'Entry updated successfully'})

@journal_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
@AccessControl.token_required
def delete_entry(current_user, entry_id):
    """Delete a journal entry"""
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Entry deleted successfully'})

@journal_bp.route('/moods', methods=['GET'])
@AccessControl.token_required
def get_mood_summary(current_user):
    """Get summary of user moods over time"""
    entries = JournalEntry.query.filter_by(user_id=current_user.id).all()
    
    mood_counts = {}
    for entry in entries:
        if entry.mood:
            mood_counts[entry.mood] = mood_counts.get(entry.mood, 0) + 1
    
    return jsonify({
        'mood_summary': mood_counts,
        'total_entries': len(entries)
    })