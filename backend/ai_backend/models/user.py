# backend/ai_backend/models/user.py

from extensions import db
from datetime import datetime

class User(db.Model):
    """User model to store basic user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    language_preference = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = db.relationship('Interaction', backref='user', lazy=True)
    progress_records = db.relationship('Progress', backref='user', lazy=True)

    # Add to backend/ai_backend/models/user.py in the User class
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'