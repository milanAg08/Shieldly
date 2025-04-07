# backend/ai_backend/chatbot/engine.py

from flask import Blueprint

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/response', methods=['POST'])
def get_response():
    # Your chatbot logic here
    return "Chatbot response"
