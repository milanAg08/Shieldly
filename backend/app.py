# backend/app.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object('config.DevelopmentConfig')

    # Register blueprints
    from ai_backend.chatbot.engine import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

    from ai_backend.adaptive_learning.routes import adaptive_learning_bp
    app.register_blueprint(adaptive_learning_bp, url_prefix='/adaptive')

    from ai_backend.security.routes import security_bp
    app.register_blueprint(security_bp, url_prefix='/security')
    # Additional blueprint registrations can go here

    return app
