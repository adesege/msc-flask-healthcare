#!/usr/bin/env python3
"""
Healthcare Survey Application Entry Point
Flask application for collecting and analyzing healthcare spending data
"""

import os
import sys
from app import create_app

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create Flask application instance for Gunicorn
app = create_app()

def main():
    """Main application entry point"""
    
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    
    # Print startup information
    print("="*60)
    print("🏥 HEALTHCARE SURVEY APPLICATION")
    print("="*60)
    print(f"🌐 Server: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"📊 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    if hasattr(app, 'db') and app.db is not None:
        print("✅ MongoDB: Connected")
    else:
        print("❌ MongoDB: Connection failed")
        print("⚠️  The application will run but data won't be saved")
    
    print("="*60)
    print()
    
    # Run the application
    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()