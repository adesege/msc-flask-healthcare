from flask import Flask
from pymongo import MongoClient
import os


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://mongodb:27017/healthcare_survey')
    
    # Initialize MongoDB connection
    try:
        client = MongoClient(app.config['MONGO_URI'])
        app.db = client.healthcare_survey
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        app.db = None
    
    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app