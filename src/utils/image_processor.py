"""
Image Processing Utilities
Handles image loading, preprocessing, and face extraction
"""
import cv2
import numpy as np
import os
import sys
from typing import Optional, Tuple
import logging
from pathlib import Path

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import FaceRecognitionConfig

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Image processing utilities for face recognition
    """
    
    def __init__(self, config: FaceRecognitionConfig = None):
        self.config = config or FaceRecognitionConfig()
        
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image with Unicode path support
        
        Args:
            image_path: Path to image file
            
        Returns:
            Loaded image or None if failed
        """
        try:
            # Use numpy to read image with Unicode path support
            image = cv2.imdecode(
                np.fromfile(image_path, dtype=np.uint8), 
                cv2.IMREAD_COLOR
            )
            return image
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    
    def is_image_file(self, filename: str) -> bool:
        """
        Check if file is a supported image format
        
        Args:
            filename: Name of the file
            
        Returns:
            True if supported image file
        """
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    
    def extract_face_roi(self, gray_image: np.ndarray, x: int, y: int, 
                        w: int, h: int, padding: int = 20) -> np.ndarray:
        """
        Extract face region of interest with padding
        
        Args:
            gray_image: Grayscale input image
            x, y, w, h: Face bounding box coordinates
            padding: Padding around face region
            
        Returns:
            Extracted and normalized face ROI
        """
        # Add padding to face region
        y1 = max(0, y - padding)
        y2 = min(gray_image.shape[0], y + h + padding)
        x1 = max(0, x - padding)
        x2 = min(gray_image.shape[1], x + w + padding)
        
        # Extract face region
        face_roi = gray_image[y1:y2, x1:x2]
        
        # Resize to standard size for consistency
        face_roi = cv2.resize(face_roi, self.config.FACE_SIZE_NORMALIZED)
        
        return face_roi
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better face detection
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Histogram equalization for better contrast
        gray = cv2.equalizeHist(gray)
        
        # Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        
        return gray
    
    def resize_image(self, image: np.ndarray, max_width: int = 800, 
                    max_height: int = 600) -> np.ndarray:
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image: Input image
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            Resized image
        """
        h, w = image.shape[:2]
        
        # Calculate scaling factor
        scale = min(max_width / w, max_height / h)
        
        if scale < 1:
            new_w = int(w * scale)
            new_h = int(h * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        return image
    
    def enhance_image_quality(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image quality for better face detection
        
        Args:
            image: Input image
            
        Returns:
            Enhanced image
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Split channels
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        lab = cv2.merge([l, a, b])
        
        # Convert back to BGR
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def validate_image(self, image: np.ndarray) -> Tuple[bool, str]:
        """
        Validate image for face recognition processing
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if image is None:
            return False, "Image is None"
        
        if len(image.shape) not in [2, 3]:
            return False, "Invalid image dimensions"
        
        h, w = image.shape[:2]
        
        if w < 50 or h < 50:
            return False, "Image too small (minimum 50x50 pixels)"
        
        if w > 4000 or h > 4000:
            return False, "Image too large (maximum 4000x4000 pixels)"
        
        return True, "Valid image"
