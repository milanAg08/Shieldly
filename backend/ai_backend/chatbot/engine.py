# backend/ai_backend/chatbot/engine.py

from flask import Blueprint, request, jsonify
import json
import re
from datetime import datetime

from backend.extensions import db
from ai_backend.models.interaction import Interaction
from ai_backend.models.user import User
from ai_backend.chatbot.safety_responses import get_safety_response
from ai_backend.chatbot.multilingual import translate_text, detect_language

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/response', methods=['POST'])
def get_response():
    """Process user query and return appropriate response"""
    data = request.get_json()
    
    if not data or 'query' not in data or 'user_id' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    user_query = data['query']
    user_id = data['user_id']
    
    # Find user or return error
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Detect language if not specified
    lang = data.get('language', user.language_preference)
    
    # If input is not in English, translate for processing
    original_language = detect_language(user_query)
    if original_language != 'en':
        query_for_processing = translate_text(user_query, source=original_language, target='en')
    else:
        query_for_processing = user_query
    
    # Determine query type and sentiment
    query_type = determine_query_type(query_for_processing)
    sentiment = analyze_sentiment(query_for_processing)
    
    # Get appropriate response
    if query_type == 'safety_question':
        response_text = get_safety_response(query_for_processing)
    else:
        response_text = get_general_response(query_for_processing)
    
    # Translate response back if needed
    if original_language != 'en':
        response_text = translate_text(response_text, source='en', target=original_language)
    
    # Store interaction in database
    new_interaction = Interaction(
        user_id=user_id,
        query=user_query,
        response=response_text,
        query_type=query_type,
        sentiment=sentiment
    )
    db.session.add(new_interaction)
    db.session.commit()
    
    # Update user's last active timestamp
    user.last_active = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        "response": response_text,
        "query_type": query_type,
        "sentiment": sentiment
    })

def determine_query_type(query):
    """Determine the type of query based on content analysis"""
    # List of keywords related to safety questions
    safety_keywords = [
        'abuse', 'assault', 'harassment', 'threat', 'violence', 'inappropriate',
        'touch', 'unsafe', 'uncomfortable', 'help', 'danger', 'scared', 'afraid',
        'consent', 'boundaries', 'protect', 'tell someone', 'report'
    ]
    
    # Check if query contains safety keywords
    for keyword in safety_keywords:
        if re.search(r'\b' + keyword + r'\b', query.lower()):
            return 'safety_question'
    
    return 'general'

def analyze_sentiment(query):
    """Basic sentiment analysis to detect user emotional state"""
    # Simplified sentiment analysis - in a real app, use a proper NLP library
    negative_words = ['scared', 'afraid', 'worried', 'anxious', 'sad', 'upset', 
                      'confused', 'hurt', 'alone', 'helpless', 'threatened']
    
    neutral_words = ['what', 'how', 'when', 'where', 'who', 'which', 'why', 
                     'information', 'explain', 'tell', 'know']
    
    urgent_words = ['emergency', 'help', 'now', 'dangerous', 'immediately', 'urgent']
    
    # Count occurrences of each type of word
    negative_count = sum(1 for word in negative_words if re.search(r'\b' + word + r'\b', query.lower()))
    neutral_count = sum(1 for word in neutral_words if re.search(r'\b' + word + r'\b', query.lower()))
    urgent_count = sum(1 for word in urgent_words if re.search(r'\b' + word + r'\b', query.lower()))
    
    # Determine sentiment based on counts
    if urgent_count > 0:
        return 'urgent'
    elif negative_count > neutral_count:
        return 'concerned'
    else:
        return 'neutral'

def get_general_response(query):
    """Generate general responses for non-safety queries"""
    # In a real application, this would use a more sophisticated NLP model
    if 'hello' in query.lower() or 'hi' in query.lower():
        return "Hello! I'm here to provide information and support. How can I help you today?"
    
    elif 'who are you' in query.lower() or 'what is shieldly' in query.lower():
        return "I'm an AI assistant from Shieldly. We're dedicated to providing education and support around sexual abuse awareness."
    
    elif 'how does this work' in query.lower() or 'what can you do' in query.lower():
        return "You can ask me questions about personal safety, boundaries, and related topics. I can provide information, resources, and support."
    
    else:
        return "I'm not sure I understand your question. Could you try rephrasing it? If you need information about personal safety or resources, please let me know."