# backend/create_db.py

from app import create_app
from extensions import db

# Create an application context
app = create_app()
with app.app_context():
    # Create all tables defined in models
    db.create_all()
    print("All database tables have been created successfully.")