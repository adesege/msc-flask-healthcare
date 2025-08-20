import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://mongodb:27017/healthcare_survey'
    MONGO_DB = 'healthcare_survey'
    MONGO_COLLECTION = 'survey_responses'
    
    # Application Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/healthcare_survey'


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/healthcare_survey_test'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
