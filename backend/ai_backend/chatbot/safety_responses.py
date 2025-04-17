# backend/ai_backend/chatbot/safety_responses.py

import re
import json
import os

# Path to the responses JSON file
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'safety_responses.json')

# Load responses from JSON file
def load_responses():
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(RESPONSES_FILE), exist_ok=True)
    
    # If file doesn't exist, create it with default responses
    if not os.path.exists(RESPONSES_FILE):
        default_responses = {
            "abuse_identification": [
                "Abuse can take many forms including physical, emotional, sexual, and verbal. Signs may include unexplained injuries, fear, withdrawal, or changes in behavior.",
                "It's important to know that abuse is never the victim's fault, and there are resources available to help."
            ],
            "reporting": [
                "If you or someone you know is in immediate danger, please call emergency services (like 911 in the US).",
                "You can also contact a trusted adult, school counselor, or call a helpline like the National Sexual Assault Hotline at 1-800-656-HOPE (4673)."
            ],
            "boundaries": [
                "Everyone has the right to set boundaries about their body and personal space. It's okay to say no to any touch that makes you uncomfortable.",
                "Healthy boundaries are an important part of all relationships. You have the right to express your boundaries and have them respected."
            ],
            "support": [
                "Supporting someone who has experienced abuse involves listening without judgment, believing them, and helping them find professional resources.",
                "Remember that healing is a process, and everyone responds differently to trauma. Patience and consistent support are important."
            ],
            "prevention": [
                "Education and open communication are key to prevention. Learning about consent and healthy relationships can help prevent abuse.",
                "Creating environments where people feel safe to speak up when something feels wrong is an important prevention strategy."
            ],
            "fallback": [
                "This is an important topic related to personal safety. Would you like me to provide resources or more specific information?",
                "I'm here to help with information about personal safety and support resources. Could you tell me more about what you'd like to know?"
            ]
        }
        
        with open(RESPONSES_FILE, 'w') as f:
            json.dump(default_responses, f, indent=4)
        
        return default_responses
    
    # Load responses from file
    try:
        with open(RESPONSES_FILE, 'r') as f:
            return json.load(f)
    except:
        # If file is corrupted, return default empty dict
        return {}

# Map of keywords to response categories
KEYWORD_MAPPING = {
    "abuse_identification": ["what is abuse", "recognize abuse", "signs of abuse", "identify abuse", "types of abuse"],
    "reporting": ["report abuse", "tell someone", "call for help", "how to report", "who to tell"],
    "boundaries": ["personal boundaries", "saying no", "consent", "body autonomy", "personal space"],
    "support": ["help someone", "support victim", "friend was abused", "family member abused"],
    "prevention": ["prevent abuse", "stop abuse", "education", "training", "awareness"]
}

def get_safety_response(query):
    """Get appropriate safety response based on query content"""
    # Load responses
    responses = load_responses()
    
    # Lowercase the query for easier matching
    query_lower = query.lower()
    
    # Find matching category
    selected_category = None
    
    # Check for exact category matches first
    for category, keywords in KEYWORD_MAPPING.items():
        for keyword in keywords:
            if keyword in query_lower:
                selected_category = category
                break
        if selected_category:
            break
    
    # If no exact match, try more general pattern matching
    if not selected_category:
        if re.search(r'\b(what|how|sign|recognize|identify)\b.*(abuse)', query_lower):
            selected_category = "abuse_identification"
        elif re.search(r'\b(report|tell|call|help|hotline)\b', query_lower):
            selected_category = "reporting"
        elif re.search(r'\b(boundary|boundaries|consent|say no|touch|space)\b', query_lower):
            selected_category = "boundaries"
        elif re.search(r'\b(help|support|friend|victim|survivor)\b', query_lower):
            selected_category = "support"
        elif re.search(r'\b(prevent|stop|education|teach|learn)\b', query_lower):
            selected_category = "prevention"
        else:
            selected_category = "fallback"
    
    # Get response from selected category
    if selected_category in responses and responses[selected_category]:
        # Select first response in the category (in a more advanced system, you could rotate responses)
        return responses[selected_category][0]
    else:
        # Fallback response if category not found
        return "I'm here to provide information about personal safety. Could you please be more specific about what you'd like to know?"