# backend/ai_backend/adaptive_learning/routes.py

from flask import Blueprint, jsonify, request
from extensions import db

from ai_backend.adaptive_learning.quiz_analyzer import QuizAnalyzer
from ai_backend.adaptive_learning.emotional_tracking import EmotionalTracker
from ai_backend.adaptive_learning.user_progress import UserProgressTracker

# Create a Blueprint named 'adaptive_learning'
adaptive_learning_bp = Blueprint('adaptive_learning', __name__)

# Quiz results endpoint
@adaptive_learning_bp.route('/quiz-results', methods=['POST'])
def process_quiz_results():
    """Process quiz results and return adaptive feedback"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'module_id' not in data or 'score' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    user_id = data['user_id']
    module_id = data['module_id']
    score = float(data['score'])
    time_taken = int(data.get('time_taken', 0))
    
    try:
        analyzer = QuizAnalyzer(user_id)
        result = analyzer.analyze_quiz_result(module_id, score, time_taken)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to process quiz results", "details": str(e)}), 500

# Emotional state tracking endpoint
@adaptive_learning_bp.route('/emotional-state', methods=['POST'])
def track_emotional_state():
    """Record user emotional state and return adaptive response"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'module_id' not in data or 'emotional_state' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    user_id = data['user_id']
    module_id = data['module_id']
    emotional_state = data['emotional_state']
    
    try:
        tracker = EmotionalTracker(user_id)
        result = tracker.track_emotional_state(module_id, emotional_state)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to track emotional state", "details": str(e)}), 500

# User activity tracking endpoint
@adaptive_learning_bp.route('/track-activity', methods=['POST'])
def track_user_activity():
    """Record user activity in a module"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'module_id' not in data or 'time_spent' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    user_id = data['user_id']
    module_id = data['module_id']
    time_spent = int(data['time_spent'])
    
    try:
        tracker = UserProgressTracker(user_id)
        result = tracker.track_activity(module_id, time_spent)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to track activity", "details": str(e)}), 500

# Get user progress summary endpoint
@adaptive_learning_bp.route('/progress-summary/<int:user_id>', methods=['GET'])
def get_progress_summary(user_id):
    """Get summary of user progress across all modules"""
    try:
        tracker = UserProgressTracker(user_id)
        result = tracker.get_progress_summary()
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to get progress summary", "details": str(e)}), 500

# Get detailed module progress endpoint
@adaptive_learning_bp.route('/module-progress/<int:user_id>/<path:module_id>', methods=['GET'])
def get_module_progress(user_id, module_id):
    """Get detailed progress for a specific module"""
    try:
        tracker = UserProgressTracker(user_id)
        result = tracker.get_module_progress(module_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to get module progress", "details": str(e)}), 500

# Get learning recommendations endpoint
@adaptive_learning_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get personalized learning recommendations"""
    try:
        tracker = UserProgressTracker(user_id)
        result = tracker.get_learning_recommendations()
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to get recommendations", "details": str(e)}), 500

# Get emotional trend analysis endpoint
@adaptive_learning_bp.route('/emotional-trend/<int:user_id>', methods=['GET'])
def get_emotional_trend(user_id):
    """Get analysis of user's emotional trends"""
    try:
        tracker = EmotionalTracker(user_id)
        result = tracker.analyze_emotional_trend()
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to get emotional trend analysis", "details": str(e)}), 500

# Get learning path endpoint
@adaptive_learning_bp.route('/learning-path/<int:user_id>', methods=['GET'])
def get_learning_path(user_id):
    """Get personalized learning path"""
    try:
        analyzer = QuizAnalyzer(user_id)
        result = analyzer.get_learning_path()
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to get learning path", "details": str(e)}), 500