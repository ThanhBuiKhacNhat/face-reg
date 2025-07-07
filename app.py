"""
Face Recognition Web Application

A professional Computer Vision application for real-time face recognition
using OpenCV and Flask. Supports 5-10 people recognition with web interface.

Author: Face Recognition Team
Date: 2025-07-06
"""

import os
import sys
from flask import Flask

# Add src to Python path for module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import configuration
from config.settings import Config

# Import Flask application factory
from src.app_factory import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Development server settings
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT,
        threaded=True
    )
