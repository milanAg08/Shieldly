# backend/ai_backend/models/progress.py

from extensions import db
from datetime import datetime

class Progress(db.Model):
    """Model to track user progress through modules and quizzes"""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.String(50), nullable=False)
    
    # Progress tracking
    completion_percentage = db.Column(db.Float, default=0.0)
    time_spent = db.Column(db.Integer, default=0)  # in seconds
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Emotional response tracking
    emotional_state = db.Column(db.String(20), nullable=True)
    
    # Quiz results
    quiz_score = db.Column(db.Float, nullable=True)
    quiz_time_taken = db.Column(db.Integer, nullable=True)  # in seconds
    
    def __repr__(self):
        return f'<Progress for User {self.user_id} on Module {self.module_id}>'