"""
Unit tests for Face Recognition System
"""
import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestFaceRecognitionModel(unittest.TestCase):
    """Test cases for FaceRecognitionModel"""
    
    def setUp(self):
        """Set up test fixtures"""
        from models.face_recognition_model import FaceRecognitionModel
        self.model = FaceRecognitionModel()
    
    def test_model_initialization(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.model.face_cascade)
        self.assertIsNotNone(self.model.face_recognizer)
    
    def test_known_faces_list(self):
        """Test known faces list"""
        known_faces = self.model.get_known_faces()
        self.assertIsInstance(known_faces, list)

class TestImageProcessor(unittest.TestCase):
    """Test cases for ImageProcessor"""
    
    def setUp(self):
        """Set up test fixtures"""
        from utils.image_processor import ImageProcessor
        self.processor = ImageProcessor()
    
    def test_processor_initialization(self):
        """Test processor initialization"""
        self.assertIsNotNone(self.processor)

class TestPeopleManager(unittest.TestCase):
    """Test cases for PeopleManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        from utils.people_manager import PeopleManager
        self.manager = PeopleManager()
    
    def test_manager_initialization(self):
        """Test manager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertIsInstance(self.manager.people_info, dict)

class TestDataAugmentation(unittest.TestCase):
    """Test cases for DataAugmentation"""
    
    def setUp(self):
        """Set up test fixtures"""
        from utils.augmentation import DataAugmentation
        self.augmenter = DataAugmentation()
    
    def test_augmentation_initialization(self):
        """Test augmentation initialization"""
        self.assertIsNotNone(self.augmenter)

if __name__ == '__main__':
    unittest.main()
