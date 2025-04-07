# backend/app.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object('config.DevelopmentConfig')

    # Register blueprints
    from ai_backend.chatbot.engine import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(adaptive_learning_bp, url_prefix='/adaptive')
    # Additional blueprint registrations can go here

    return app
