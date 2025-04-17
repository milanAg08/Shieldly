# backend/tests/test_chatbot.py

import unittest
from backend.ai_backend.chatbot.engine import ChatbotEngine
from backend.ai_backend.chatbot.multilingual import translate_text, detect_language

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = ChatbotEngine()
    
    def test_safety_question_response(self):
        """Test chatbot responds appropriately to safety questions"""
        test_questions = [
            "What should I do if I feel unsafe?",
            "How do I report bullying?",
            "What are warning signs of abuse?"
        ]
        
        for question in test_questions:
            response = self.chatbot.get_response(question)
            self.assertIsNotNone(response)
            self.assertTrue(len(response) > 20)
    
    def test_non_safety_question(self):
        """Test chatbot responds appropriately to non-safety questions"""
        response = self.chatbot.get_response("Tell me about the weather")
        self.assertIn("I'm designed to help with safety questions", response)
    
    def test_language_detection(self):
        """Test language detection functionality"""
        spanish_text = "¿Qué debo hacer si me siento inseguro?"
        detected = detect_language(spanish_text)
        self.assertEqual(detected, "es")
    
    def test_translation(self):
        """Test translation functionality"""
        english_text = "What should I do if I feel unsafe?"
        spanish_translation = translate_text(english_text, "es")
        self.assertNotEqual(english_text, spanish_translation)
        self.assertIn("inseguro", spanish_translation)

if __name__ == '__main__':
    unittest.main()