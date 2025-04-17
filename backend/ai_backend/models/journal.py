# backend/ai_backend/models/journal.py

from backend.extensions import db
from datetime import datetime

class JournalEntry(db.Model):
    """Model to store user journal entries"""
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    mood = db.Column(db.String(20), nullable=True)
    content = db.Column(db.Text, nullable=False)
    
    # Whether entry should be encrypted
    is_sensitive = db.Column(db.Boolean, default=False)
    
    # Encrypted content (if sensitive)
    encrypted_content = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<JournalEntry {self.id} from User {self.user_id}>'