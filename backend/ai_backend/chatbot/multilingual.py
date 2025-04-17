# backend/ai_backend/chatbot/multilingual.py

import re
import json
import os

# In a production environment, you would use a proper translation API
# This is a simplified implementation for demonstration purposes

# Path to the language files
LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), 'data', 'languages')

# Supported languages with their codes
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German'
}

# Ensure language directory exists
os.makedirs(LANGUAGE_DIR, exist_ok=True)

def detect_language(text):
    """
    Detect the language of the input text
    In a real implementation, use a language detection library
    """
    # Very simple language detection based on common words
    # In a real app, use a proper language detection library like langdetect
    
    text_lower = text.lower()
    
    # Spanish indicators
    spanish_words = ['como', 'qué', 'por qué', 'cómo', 'ayuda', 'hola', 'gracias']
    if any(word in text_lower for word in spanish_words):
        return 'es'
    
    # French indicators
    french_words = ['comment', 'pourquoi', 'bonjour', 'merci', 'aide', 'je suis']
    if any(word in text_lower for word in french_words):
        return 'fr'
    
    # German indicators
    german_words = ['wie', 'warum', 'hallo', 'danke', 'hilfe', 'ich bin']
    if any(word in text_lower for word in german_words):
        return 'de'
    
    # Default to English
    return 'en'

def load_translation_dictionary(language_code):
    """Load translation dictionary for a specific language"""
    # Path to the translation file
    file_path = os.path.join(LANGUAGE_DIR, f'{language_code}.json')
    
    # If file doesn't exist, create it with empty dictionary
    if not os.path.exists(file_path):
        # Create sample translation data for demonstration
        sample_data = {}
        
        if language_code == 'es':
            sample_data = {
                "Hello": "Hola",
                "Help": "Ayuda",
                "I'm here to help": "Estoy aquí para ayudar",
                "How can I assist you": "¿Cómo puedo ayudarte?",
                "abuse": "abuso",
                "report": "informar",
                "emergency": "emergencia",
                "safety": "seguridad",
                "support": "apoyo"
            }
        elif language_code == 'fr':
            sample_data = {
                "Hello": "Bonjour",
                "Help": "Aide",
                "I'm here to help": "Je suis là pour aider",
                "How can I assist you": "Comment puis-je vous aider?",
                "abuse": "abus",
                "report": "signaler",
                "emergency": "urgence",
                "safety": "sécurité",
                "support": "soutien"
            }
        elif language_code == 'de':
            sample_data = {
                "Hello": "Hallo",
                "Help": "Hilfe",
                "I'm here to help": "Ich bin hier, um zu helfen",
                "How can I assist you": "Wie kann ich Ihnen helfen?",
                "abuse": "Missbrauch",
                "report": "melden",
                "emergency": "Notfall",
                "safety": "Sicherheit",
                "support": "Unterstützung"
            }
        
        with open(file_path, 'w') as f:
            json.dump(sample_data, f, indent=4)
        
        return sample_data
    
    # Load translations from file
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        # If file is corrupted, return empty dict
        return {}

def translate_text(text, source='en', target='es'):
    """
    Translate text from source language to target language
    
    In a production environment, you would use a proper translation API
    like Google Translate, Microsoft Translator, or DeepL.
    """
    # If source and target are the same, no translation needed
    if source == target:
        return text
    
    # If target is English and we're translating to English, just return the text
    if target == 'en':
        return text
    
    # Load translation dictionary
    translation_dict = load_translation_dictionary(target)
    
    # For demonstration, we'll do a simple word-by-word replacement
    # This is NOT how real translation works, but serves for demonstration
    result = text
    
    # Sort translations by length (descending) to handle phrases before single words
    sorted_translations = sorted(translation_dict.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Replace each known phrase/word with its translation
    for eng, trans in sorted_translations:
        pattern = r'\b' + re.escape(eng) + r'\b'
        result = re.sub(pattern, trans, result, flags=re.IGNORECASE)
    
    return result

def get_supported_languages():
    """Return list of supported languages"""
    return SUPPORTED_LANGUAGES