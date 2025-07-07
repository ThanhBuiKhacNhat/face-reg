"""
Face Recognition System Configuration
"""
import os
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "dataset"
CAPTURES_DIR = PROJECT_ROOT / "captures"
CONFIG_DIR = PROJECT_ROOT / "config"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"

# Face Recognition Settings
class FaceRecognitionConfig:
    # Model settings
    CONFIDENCE_THRESHOLD = 100
    MIN_FACE_SIZE = (50, 50)
    FACE_CASCADE_FILE = "haarcascade_frontalface_default.xml"
    FACE_SIZE_NORMALIZED = (100, 100)
    
    # Data augmentation
    USE_AUGMENTATION = True
    AUGMENTATION_FACTOR = 2
    
    # Augmentation parameters
    ROTATION_RANGE = (-15, 15)  # degrees
    BRIGHTNESS_RANGE = (0.7, 1.3)
    CONTRAST_RANGE = (0.8, 1.2)
    FLIP_PROBABILITY = 0.5
    NOISE_STD = 5
    TRANSLATION_RANGE = (-5, 5)  # pixels
    
    # Training quality thresholds
    QUALITY_THRESHOLDS = {
        "excellent": 3,  # 3+ images = ⭐⭐⭐
        "good": 2,       # 2 images = ⭐⭐
        "basic": 1       # 1 image = ⭐
    }

# Flask App Settings
class AppConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'face-recognition-secret-key-2025')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database/Storage Settings
class StorageConfig:
    PEOPLE_INFO_FILE = PROJECT_ROOT / "config" / "people_info.json"
    DATASET_PATH = DATA_DIR
    CAPTURES_PATH = CAPTURES_DIR
    
    # Ensure directories exist
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATASET_PATH,
            cls.CAPTURES_PATH,
            CONFIG_DIR,
            TEMPLATES_DIR,
            STATIC_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Logging Configuration
class LogConfig:
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = PROJECT_ROOT / "logs" / "face_recognition.log"

# Main Configuration Class
class Config:
    """Main configuration class that combines all settings"""
    
    # Include all sub-configurations
    FACE_RECOGNITION = FaceRecognitionConfig
    APP = AppConfig
    STORAGE = StorageConfig
    LOG = LogConfig
    
    # Quick access to commonly used settings
    SECRET_KEY = AppConfig.SECRET_KEY
    DEBUG = AppConfig.DEBUG
    HOST = AppConfig.HOST
    PORT = AppConfig.PORT
    
    CONFIDENCE_THRESHOLD = FaceRecognitionConfig.CONFIDENCE_THRESHOLD
    USE_AUGMENTATION = FaceRecognitionConfig.USE_AUGMENTATION
    
    DATASET_PATH = StorageConfig.DATASET_PATH
    PEOPLE_INFO_FILE = StorageConfig.PEOPLE_INFO_FILE
    
    @classmethod
    def init_app(cls):
        """Initialize application directories and logging"""
        # Ensure directories exist
        cls.STORAGE.ensure_directories()
        
        # Create logs directory
        logs_dir = PROJECT_ROOT / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        return cls
