# backend/ai_backend/adaptive_learning/emotional_tracking.py

from backend.extensions import db
from backend.ai_backend.models.progress import Progress
from ai_backend.models.interaction import Interaction
from ai_backend.models.user import User
from datetime import datetime, timedelta
import re

class EmotionalTracker:
    """Tracks and analyzes user emotional state during interactions"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = User.query.get(user_id)
        if not self.user:
            raise ValueError(f"User with ID {user_id} not found")
    
    def track_emotional_state(self, module_id, emotional_state):
        """
        Record user's emotional state for a specific module
        
        Args:
            module_id (str): The module identifier
            emotional_state (str): User's emotional state (e.g., 'anxious', 'confident')
        
        Returns:
            dict: Updated emotional tracking information
        """
        # Find or create progress record
        progress = Progress.query.filter_by(
            user_id=self.user_id,
            module_id=module_id
        ).first()
        
        if not progress:
            progress = Progress(
                user_id=self.user_id,
                module_id=module_id,
                completion_percentage=0.0,
                time_spent=0,
                last_activity=datetime.utcnow()
            )
            db.session.add(progress)
        
        # Update emotional state
        progress.emotional_state = emotional_state
        progress.last_activity = datetime.utcnow()
        db.session.commit()
        
        # Generate appropriate response based on emotional state
        response = self._generate_emotional_support(emotional_state)
        
        return {
            'recorded_state': emotional_state,
            'support_response': response,
            'adaptation': self._get_content_adaptation(emotional_state)
        }
    
    def analyze_emotional_trend(self):
        """
        Analyze emotional trends across recent interactions
        
        Returns:
            dict: Analysis of emotional trends and recommendations
        """
        # Get recent interactions (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_interactions = Interaction.query.filter_by(
            user_id=self.user_id
        ).filter(
            Interaction.timestamp >= week_ago
        ).all()
        
        # Extract sentiment data
        sentiments = [interaction.sentiment for interaction in recent_interactions if interaction.sentiment]
        
        # Count occurrences of each sentiment
        sentiment_counts = {}
        for sentiment in sentiments:
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        # Determine dominant sentiment
        dominant_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])[0] if sentiment_counts else 'neutral'
        
        # Generate recommendations based on emotional trend
        recommendations = self._generate_trend_recommendations(dominant_sentiment, sentiment_counts)
        
        return {
            'sentiment_counts': sentiment_counts,
            'dominant_sentiment': dominant_sentiment,
            'trend': self._determine_trend(sentiments),
            'recommendations': recommendations
        }
    
    def _determine_trend(self, sentiments):
        """Determine if emotional state is improving, worsening, or stable"""
        if not sentiments or len(sentiments) < 3:
            return "insufficient_data"
        
        # Simplified trend analysis - in a real system, use more sophisticated methods
        # Map sentiments to numerical values
        sentiment_values = {
            'neutral': 0,
            'concerned': -1,
            'urgent': -2
        }
        
        # Convert sentiments to numerical values
        values = [sentiment_values.get(s, 0) for s in sentiments]
        
        # Calculate trend (positive slope = improving, negative = worsening)
        if sum(values[:len(values)//2]) < sum(values[len(values)//2:]):
            return "improving"
        elif sum(values[:len(values)//2]) > sum(values[len(values)//2:]):
            return "worsening"
        else:
            return "stable"
    
    def _generate_emotional_support(self, emotional_state):
        """Generate supportive response based on emotional state"""
        if emotional_state in ['anxious', 'worried', 'scared', 'nervous']:
            return "It's completely normal to feel anxious about this topic. Remember that learning about safety gives you tools to protect yourself and others."
        
        elif emotional_state in ['sad', 'upset', 'depressed']:
            return "This can be difficult material to process. If you're feeling overwhelmed, consider taking a break or talking to someone you trust."
        
        elif emotional_state in ['confused', 'uncertain']:
            return "This material can be complex. Let's break it down into smaller pieces to make it easier to understand."
        
        elif emotional_state in ['confident', 'empowered']:
            return "Great to hear you're feeling confident! Knowledge is empowering, and understanding these concepts helps create safer communities."
        
        elif emotional_state in ['interested', 'curious']:
            return "Your curiosity shows a commitment to learning. This knowledge will help you be an advocate for yourself and others."
        
        else:
            return "Thank you for sharing how you're feeling. Recognizing our emotions is an important part of the learning process."
    
    def _get_content_adaptation(self, emotional_state):
        """Determine how to adapt content based on emotional state"""
        adaptations = {}
        
        if emotional_state in ['anxious', 'worried', 'scared', 'nervous']:
            adaptations['pace'] = 'slower'
            adaptations['content_detail'] = 'simplified'
            adaptations['supportive_elements'] = ['reassurance', 'breaks']
        
        elif emotional_state in ['sad', 'upset', 'depressed']:
            adaptations['tone'] = 'gentle'
            adaptations['supportive_elements'] = ['encouragement', 'resources']
            adaptations['additional_content'] = ['coping_strategies']
        
        elif emotional_state in ['confused', 'uncertain']:
            adaptations['pace'] = 'slower'
            adaptations['content_detail'] = 'simplified'
            adaptations['additional_content'] = ['examples', 'visuals']
        
        elif emotional_state in ['confident', 'empowered']:
            adaptations['pace'] = 'faster'
            adaptations['content_detail'] = 'advanced'
            adaptations['additional_content'] = ['case_studies', 'action_steps']
        
        elif emotional_state in ['interested', 'curious']:
            adaptations['additional_content'] = ['deeper_dive', 'related_topics']
        
        return adaptations
    
    def _generate_trend_recommendations(self, dominant_sentiment, sentiment_counts):
        """Generate recommendations based on emotional trends"""
        recommendations = []
        
        if dominant_sentiment == 'concerned':
            recommendations.append("Consider incorporating more reassurance and supportive content")
            recommendations.append("Offer simpler, more manageable learning segments")
        
        elif dominant_sentiment == 'urgent':
            recommendations.append("Provide clear, direct access to support resources")
            recommendations.append("Offer immediate tools and strategies for safety")
        
        elif dominant_sentiment == 'neutral' and sentiment_counts.get('neutral', 0) > 5:
            # Consistently neutral might indicate emotional disconnection
            recommendations.append("Introduce more engaging, personally relevant content")
            recommendations.append("Incorporate stories and real-world examples to foster connection")
        
        # Add general recommendation
        recommendations.append("Regularly check in about emotional state during challenging topics")
        
        return recommendations