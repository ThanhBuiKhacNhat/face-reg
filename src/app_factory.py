"""
Flask Application Factory

Creates and configures the Flask application with all necessary components.
"""

import os
from flask import Flask, render_template

# Import configuration
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import Config

# Import API blueprints
from .api.routes import api_bp

# Import models and managers
from .models.face_recognition_model import FaceRecognitionModel
from .utils.people_manager import PeopleManager


def create_app(config_class=Config):
    """
    Application factory function that creates and configures Flask app.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize face recognition model
    face_model = FaceRecognitionModel()
    people_manager = PeopleManager()
    
    # Store in app context for access in routes
    app.face_model = face_model
    app.people_manager = people_manager
    
    # Register API blueprints
    app.register_blueprint(api_bp)
    
    # Main route
    @app.route('/')
    def index():
        """Main page route"""
        known_faces = face_model.get_known_faces()
        return render_template('index.html', known_faces=known_faces)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        return {'error': 'Page not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return {'error': 'Internal server error'}, 500
    
    return app
