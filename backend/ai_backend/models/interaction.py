# backend/ai_backend/models/interaction.py

from extensions import db
from datetime import datetime

class Interaction(db.Model):
    """Model to store chatbot interactions"""
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Store metadata about the interaction
    query_type = db.Column(db.String(50), nullable=True)  # e.g., 'safety_question', 'general'
    sentiment = db.Column(db.String(20), nullable=True)   # e.g., 'neutral', 'concerned'
    
    def __repr__(self):
        return f'<Interaction {self.id} from User {self.user_id}>'