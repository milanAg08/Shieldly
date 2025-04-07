# backend/app.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object('config.Config')

    # Register blueprints
    from ai_backend.chatbot.engine import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

    # Additional blueprint registrations can go here

    return app
