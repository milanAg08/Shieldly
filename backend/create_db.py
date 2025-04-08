from .app import create_app
from .extensions import db

# Create an application context
app = create_app()
with app.app_context():
    # Create all tables
    db.create_all()
    print("All tables have been created successfully.")
