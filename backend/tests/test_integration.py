# backend/tests/test_integration.py

import unittest
import json
from datetime import datetime
from backend.app import create_app
from backend.extensions import db
from backend.ai_backend.models.user import User
from backend.ai_backend.models.progress import Progress
from backend.ai_backend.models.journal import JournalEntry
from backend.ai_backend.models.interaction import Interaction
from backend.ai_backend.adaptive_learning.emotional_tracking import EmotionalTracker
from backend.ai_backend.adaptive_learning.user_progress import UserProgressTracker
from backend.ai_backend.chatbot.engine import ChatbotEngine
from backend.ai_backend.security.data_encryption import DataEncryption

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create test database and tables
        db.create_all()
        
        # Create test user
        test_user = User(
            username='testuser',
            email='test@example.com'
        )
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
        
        self.test_user = test_user
        
        # Create test token
        self.token = test_user.generate_auth_token()
        self.headers = {'Authorization': f'Bearer {self.token}'}
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_chatbot_response(self):
        """Test that chatbot provides safety responses"""
        # Create chatbot instance
        chatbot = ChatbotEngine()
        
        # Test with a safety-related question
        response = chatbot.get_response("What should I do if I feel unsafe?", language="en")
        
        # Verify response contains helpful safety information
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 20)  # Should be a substantial response
        
        # Test multilingual support
        spanish_response = chatbot.get_response("¿Qué debo hacer si no me siento seguro?", language="es")
        self.assertIsNotNone(spanish_response)
        self.assertTrue(len(spanish_response) > 20)
    
    def test_emotional_tracking_integration(self):
        """Test that emotional tracking affects content recommendations"""
        # Create progress record
        progress = Progress(
            user_id=self.test_user.id,
            module_id='safety_module_1',
            completion_percentage=50.0,
            time_spent=300,
            last_activity=datetime.utcnow()
        )
        db.session.add(progress)
        db.session.commit()
        
        # Track emotional state
        tracker = EmotionalTracker(self.test_user.id)
        result = tracker.track_emotional_state('safety_module_1', 'anxious')
        
        # Verify emotional state was recorded
        updated_progress = Progress.query.filter_by(
            user_id=self.test_user.id,
            module_id='safety_module_1'
        ).first()
        
        self.assertEqual(updated_progress.emotional_state, 'anxious')
        
        # Check that content adaptations are recommended
        self.assertIn('content_detail', result['adaptation'])
        self.assertEqual(result['adaptation']['content_detail'], 'simplified')
    
    def test_progress_tracking(self):
        """Test that user progress is tracked correctly"""
        # Create progress tracker
        progress_tracker = UserProgressTracker(self.test_user.id)
        
        # Track activity
        module_id = 'safety_module_2'
        result = progress_tracker.track_activity(module_id, 180)  # 3 minutes
        
        # Verify progress was recorded
        updated_progress = Progress.query.filter_by(
            user_id=self.test_user.id,
            module_id=module_id
        ).first()
        
        self.assertEqual(updated_progress.time_spent, 180)
        self.assertTrue(updated_progress.completion_percentage > 0)
        
        # Get progress summary
        summary = progress_tracker.get_progress_summary()
        self.assertEqual(summary['total_modules'], 1)
    
    def test_journal_encryption(self):
        """Test that sensitive journal entries are properly encrypted and decrypted"""
        # Post a sensitive journal entry
        response = self.client.post(
            '/api/journal/entries',
            headers=self.headers,
            json={
                'content': 'This is a sensitive entry about my feelings',
                'mood': 'anxious',
                'is_sensitive': True
            }
        )
        
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        entry_id = result['entry_id']
        
        # Retrieve the entry from database
        entry = JournalEntry.query.get(entry_id)
        
        # Verify content is encrypted (not stored as plaintext)
        self.assertIsNone(entry.content)
        self.assertIsNotNone(entry.encrypted_content)
        
        # Retrieve entry via API and verify decryption works
        response = self.client.get(
            f'/api/journal/entries/{entry_id}',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        
        # Content should be decrypted in the response
        self.assertEqual(result['content'], 'This is a sensitive entry about my feelings')
    
    def test_quiz_results_update_progress(self):
        """Test that quiz results update progress metrics"""
        # Set up a module with some initial progress
        progress = Progress(
            user_id=self.test_user.id,
            module_id='safety_module_3',
            completion_percentage=80.0,
            time_spent=300,
            last_activity=datetime.utcnow()
        )
        db.session.add(progress)
        db.session.commit()
        
        # Submit quiz results
        response = self.client.post(
            '/api/adaptive-learning/quiz-result',
            headers=self.headers,
            json={
                'module_id': 'safety_module_3',
                'quiz_id': 'quiz_1',
                'score': 85.0,
                'max_score': 100.0,
                'time_spent': 120,
                'answers': {
                    'q1': 'answer1',
                    'q2': 'answer2'
                }
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify progress was updated
        updated_progress = Progress.query.filter_by(
            user_id=self.test_user.id,
            module_id='safety_module_3'
        ).first()
        
        self.assertEqual(updated_progress.quiz_score, 85.0)
        self.assertEqual(updated_progress.completion_percentage, 100.0)  # Should be complete after quiz

if __name__ == '__main__':
    unittest.main()