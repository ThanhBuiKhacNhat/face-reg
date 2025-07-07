"""
Face Recognition Model
Handles face detection, training, and recognition using OpenCV LBPH
"""
import os
import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import logging
import sys

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import FaceRecognitionConfig
from src.utils.image_processor import ImageProcessor
from src.utils.augmentation import DataAugmentation

logger = logging.getLogger(__name__)

class FaceRecognitionModel:
    """
    Main face recognition model using OpenCV LBPH (Local Binary Pattern Histogram)
    """
    
    def __init__(self, config: FaceRecognitionConfig = None):
        self.config = config or FaceRecognitionConfig()
        
        # Initialize OpenCV components
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + self.config.FACE_CASCADE_FILE
        )
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Model state
        self.is_trained = False
        self.known_face_names = []
        self.training_stats = {}
        self.confidence_threshold = self.config.CONFIDENCE_THRESHOLD
        self.use_augmentation = self.config.USE_AUGMENTATION
        self.augmentation_factor = self.config.AUGMENTATION_FACTOR
        
        # Processors
        self.image_processor = ImageProcessor(config=self.config)
        self.augmentation = DataAugmentation(config=self.config) if self.config.USE_AUGMENTATION else None
        
        logger.info("Face Recognition Model initialized")
        
        # Auto-load faces from dataset on initialization
        try:
            from pathlib import Path
            dataset_path = Path('dataset')
            if dataset_path.exists():
                result = self.train(str(dataset_path))
                logger.info(f"Auto-trained model: {result.get('message', 'Training completed')}")
            else:
                logger.warning(f"Dataset path {dataset_path} does not exist")
        except Exception as e:
            logger.warning(f"Could not auto-train model: {e}")
    
    def extract_face_from_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Extract and preprocess face from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed face ROI or None if no face found
        """
        try:
            # Load image with Unicode support
            image = self.image_processor.load_image(image_path)
            if image is None:
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 1.1, 4, minSize=self.config.MIN_FACE_SIZE
            )
            
            if len(faces) == 0:
                return None
            
            # Get the largest face (main subject)
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            
            # Extract face region with padding
            face_roi = self.image_processor.extract_face_roi(gray, x, y, w, h)
            
            return face_roi
            
        except Exception as e:
            logger.error(f"Error extracting face from {image_path}: {e}")
            return None
    
    def load_dataset(self, dataset_path: str) -> Tuple[List[np.ndarray], List[int], Dict[str, int]]:
        """
        Load training dataset from folder structure
        
        Args:
            dataset_path: Path to dataset directory
            
        Returns:
            Tuple of (face_images, face_labels, person_image_count)
        """
        face_images = []
        face_labels = []
        person_image_count = {}
        
        if not os.path.exists(dataset_path):
            logger.warning(f"Dataset path does not exist: {dataset_path}")
            return face_images, face_labels, person_image_count
        
        # Load from folder structure (recommended)
        person_folders = self._load_from_folders(
            dataset_path, face_images, face_labels, person_image_count
        )
        
        # Load from flat file structure (legacy support)
        self._load_from_files(
            dataset_path, face_images, face_labels, person_image_count
        )
        
        logger.info(f"Loaded {len(face_images)} face images for {len(self.known_face_names)} people")
        
        return face_images, face_labels, person_image_count
    
    def _load_from_folders(self, dataset_path: str, face_images: List, 
                          face_labels: List, person_image_count: Dict) -> set:
        """Load images from person folders (recommended structure)"""
        person_folders = set()
        
        for item in os.listdir(dataset_path):
            item_path = os.path.join(dataset_path, item)
            
            # Skip files and README
            if not os.path.isdir(item_path) or item.lower() in ['readme.md', '__pycache__']:
                continue
            
            person_name = item.replace('_', ' ').title()
            person_folders.add(person_name)
            
            # Add person to known names
            if person_name not in self.known_face_names:
                self.known_face_names.append(person_name)
            
            person_label = self.known_face_names.index(person_name)
            person_image_count[person_name] = 0
            
            # Process all images in folder
            try:
                for filename in os.listdir(item_path):
                    if self.image_processor.is_image_file(filename):
                        image_path = os.path.join(item_path, filename)
                        self._process_image(
                            image_path, person_name, person_label,
                            face_images, face_labels, person_image_count
                        )
            except Exception as e:
                logger.error(f"Error processing folder {item}: {e}")
        
        return person_folders
    
    def _load_from_files(self, dataset_path: str, face_images: List,
                        face_labels: List, person_image_count: Dict):
        """Load images from flat file structure (legacy support)"""
        person_files = {}
        
        for filename in os.listdir(dataset_path):
            if self.image_processor.is_image_file(filename):
                # Extract person name
                base_name = os.path.splitext(filename)[0]
                person_name = base_name.split('_')[0] if '_' in base_name else base_name
                person_name = person_name.replace('_', ' ').title()
                
                if person_name not in person_files:
                    person_files[person_name] = []
                person_files[person_name].append(filename)
        
        # Process each person's images
        for person_name, files in person_files.items():
            if person_name not in person_image_count:
                person_image_count[person_name] = 0
            
            # Add person to known names
            if person_name not in self.known_face_names:
                self.known_face_names.append(person_name)
            
            person_label = self.known_face_names.index(person_name)
            
            for filename in files:
                image_path = os.path.join(dataset_path, filename)
                self._process_image(
                    image_path, person_name, person_label,
                    face_images, face_labels, person_image_count,
                    source_type="file"
                )
    
    def _process_image(self, image_path: str, person_name: str, person_label: int,
                      face_images: List, face_labels: List, person_image_count: Dict,
                      source_type: str = "folder"):
        """Process a single image with optional augmentation"""
        face_roi = self.extract_face_from_image(image_path)
        
        if face_roi is not None:
            if self.config.USE_AUGMENTATION and self.augmentation:
                # Apply data augmentation
                augmented_faces = self.augmentation.augment_face(
                    face_roi, num_augmentations=self.config.AUGMENTATION_FACTOR
                )
                
                for aug_face in augmented_faces:
                    face_images.append(aug_face)
                    face_labels.append(person_label)
                    person_image_count[person_name] += 1
                
                emoji = "📁" if source_type == "folder" else "📄"
                logger.info(f"{emoji} Loaded face for {person_name} from {os.path.basename(image_path)} (+ {len(augmented_faces)-1} augmented)")
            else:
                face_images.append(face_roi)
                face_labels.append(person_label)
                person_image_count[person_name] += 1
                
                emoji = "📁" if source_type == "folder" else "📄"
                logger.info(f"{emoji} Loaded face for {person_name} from {os.path.basename(image_path)}")
        else:
            emoji = "📁" if source_type == "folder" else "📄"
            logger.warning(f"{emoji} No face found in {os.path.basename(image_path)}")
    
    def train(self, dataset_path: str) -> Dict[str, Any]:
        """
        Train the face recognition model
        
        Args:
            dataset_path: Path to training dataset
            
        Returns:
            Training statistics
        """
        logger.info("Starting model training...")
        
        # Load dataset
        face_images, face_labels, person_image_count = self.load_dataset(dataset_path)
        
        if len(face_images) == 0:
            logger.warning("No face images found for training")
            self.is_trained = False
            return {"success": False, "error": "No training data found"}
        
        try:
            # Train the recognizer
            self.face_recognizer.train(face_images, np.array(face_labels))
            self.is_trained = True
            
            # Compile training statistics
            self.training_stats = self._compile_training_stats(
                face_images, person_image_count
            )
            
            logger.info("Model training completed successfully")
            return {"success": True, "stats": self.training_stats}
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            self.is_trained = False
            return {"success": False, "error": str(e)}
    
    def _compile_training_stats(self, face_images: List, person_image_count: Dict) -> Dict:
        """Compile training statistics"""
        total_faces = len(face_images)
        total_people = len(self.known_face_names)
        
        # Calculate original vs augmented counts
        original_count = 0
        for person, count in person_image_count.items():
            if self.config.USE_AUGMENTATION:
                original_images = count // (self.config.AUGMENTATION_FACTOR + 1)
                original_count += original_images
            else:
                original_count += count
        
        # Quality assessment
        quality_assessment = {}
        for person, count in person_image_count.items():
            if self.config.USE_AUGMENTATION:
                original_images = count // (self.config.AUGMENTATION_FACTOR + 1)
            else:
                original_images = count
            
            if original_images >= self.config.QUALITY_THRESHOLDS["excellent"]:
                quality = "⭐⭐⭐"
            elif original_images >= self.config.QUALITY_THRESHOLDS["good"]:
                quality = "⭐⭐"
            else:
                quality = "⭐"
            
            quality_assessment[person] = {
                "original_images": original_images,
                "total_images": count,
                "quality": quality
            }
        
        return {
            "total_faces": total_faces,
            "total_people": total_people,
            "original_count": original_count,
            "augmented_count": total_faces - original_count if self.config.USE_AUGMENTATION else 0,
            "augmentation_enabled": self.config.USE_AUGMENTATION,
            "augmentation_factor": self.config.AUGMENTATION_FACTOR,
            "quality_assessment": quality_assessment
        }
    
    def recognize_faces(self, frame: np.ndarray) -> Tuple[List[Tuple], List[str]]:
        """
        Recognize faces in a frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Tuple of (face_locations, face_names)
        """
        if not self.is_trained:
            return [], []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 1.1, 4, minSize=(30, 30)
        )
        
        face_locations = []
        face_names = []
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, self.config.FACE_SIZE_NORMALIZED)
            
            # Predict using trained model
            label, confidence = self.face_recognizer.predict(face_roi)
            
            # Determine name based on confidence
            if confidence < self.config.CONFIDENCE_THRESHOLD:
                name = self.known_face_names[label]
                confidence_percent = max(0, 100 - confidence)
                logger.debug(f"Recognized: {name} (confidence: {confidence_percent:.1f}%)")
            else:
                name = "Unknown"
                logger.debug(f"Unknown person (confidence too low: {100 - confidence:.1f}%)")
            
            # Convert to standardized format (top, right, bottom, left)
            face_locations.append((y, x + w, y + h, x))
            face_names.append(name)
        
        return face_locations, face_names
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information and statistics"""
        return {
            "is_trained": self.is_trained,
            "known_faces": self.known_face_names,
            "total_people": len(self.known_face_names),
            "confidence_threshold": self.config.CONFIDENCE_THRESHOLD,
            "training_stats": self.training_stats if hasattr(self, 'training_stats') else {},
            "config": {
                "use_augmentation": self.config.USE_AUGMENTATION,
                "augmentation_factor": self.config.AUGMENTATION_FACTOR,
                "min_face_size": self.config.MIN_FACE_SIZE,
                "face_size_normalized": self.config.FACE_SIZE_NORMALIZED
            }
        }
    
    def update_config(self, **kwargs):
        """Update model configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key.upper()):
                setattr(self.config, key.upper(), value)
                logger.info(f"Updated config: {key} = {value}")
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get comprehensive training summary with quality metrics"""
        if not self.is_trained:
            return {"success": False, "error": "Model is not trained yet"}
        
        try:
            summary = {
                "total_faces": 0,
                "total_people": len(self.known_face_names),
                "original_count": 0,
                "augmented_count": 0,
                "quality_assessment": {}
            }
            
            for person, count in self.training_stats["quality_assessment"].items():
                summary["total_faces"] += count["total_images"]
                summary["original_count"] += count["original_images"]
                summary["augmented_count"] += count["total_images"] - count["original_images"]
                
                # Add quality metric
                quality_metric = {
                    "total_images": count["total_images"],
                    "original_images": count["original_images"],
                    "augmentation_factor": count["total_images"] // count["original_images"] if count["original_images"] > 0 else 0
                }
                summary["quality_assessment"][person] = quality_metric
            
            return {"success": True, "summary": summary}
        
        except Exception as e:
            logger.error(f"Error generating training summary: {e}")
            return {"success": False, "error": str(e)}
    
    def get_known_faces(self) -> List[str]:
        """Get list of known face names"""
        return self.known_face_names.copy()
        
    def get_training_info(self) -> Dict[str, Any]:
        """Get detailed training information"""
        if not self.is_trained:
            return {"success": False, "error": "Model is not trained yet"}
        
        try:
            return {
                "success": True,
                "total_faces": self.training_stats["total_faces"],
                "total_people": self.training_stats["total_people"],
                "original_count": self.training_stats["original_count"],
                "augmented_count": self.training_stats["augmented_count"],
                "augmentation_enabled": self.config.USE_AUGMENTATION,
                "augmentation_factor": self.config.AUGMENTATION_FACTOR,
                "quality_assessment": self.training_stats["quality_assessment"]
            }
        
        except Exception as e:
            logger.error(f"Error retrieving training info: {e}")
            return {"success": False, "error": str(e)}
