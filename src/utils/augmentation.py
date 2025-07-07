"""
Data Augmentation for Face Recognition
Applies various transformations to increase training data diversity
"""
import cv2
import numpy as np
import os
import sys
from typing import List
import logging

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import FaceRecognitionConfig

logger = logging.getLogger(__name__)

class DataAugmentation:
    """
    Data augmentation utilities for face recognition training
    """
    
    def __init__(self, config: FaceRecognitionConfig = None):
        self.config = config or FaceRecognitionConfig()
        
    def augment_face(self, face_roi: np.ndarray, num_augmentations: int = 3) -> List[np.ndarray]:
        """
        Apply data augmentation to face images
        
        Args:
            face_roi: Original face region of interest
            num_augmentations: Number of augmented versions to generate
            
        Returns:
            List of augmented face images (including original)
        """
        augmented_faces = [face_roi.copy()]  # Include original
        
        for _ in range(num_augmentations):
            aug_face = face_roi.copy()
            
            # Apply random transformations
            aug_face = self._apply_rotation(aug_face)
            aug_face = self._apply_brightness(aug_face)
            aug_face = self._apply_contrast(aug_face)
            aug_face = self._apply_horizontal_flip(aug_face)
            aug_face = self._apply_noise(aug_face)
            aug_face = self._apply_translation(aug_face)
            
            augmented_faces.append(aug_face)
        
        return augmented_faces
    
    def _apply_rotation(self, image: np.ndarray) -> np.ndarray:
        """Apply random rotation within specified range"""
        angle = np.random.uniform(*self.config.ROTATION_RANGE)
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
        
        return rotated
    
    def _apply_brightness(self, image: np.ndarray) -> np.ndarray:
        """Apply random brightness adjustment"""
        brightness_factor = np.random.uniform(*self.config.BRIGHTNESS_RANGE)
        brightened = np.clip(image * brightness_factor, 0, 255).astype(np.uint8)
        
        return brightened
    
    def _apply_contrast(self, image: np.ndarray) -> np.ndarray:
        """Apply random contrast adjustment"""
        contrast_factor = np.random.uniform(*self.config.CONTRAST_RANGE)
        contrasted = np.clip(
            (image - 127.5) * contrast_factor + 127.5, 0, 255
        ).astype(np.uint8)
        
        return contrasted
    
    def _apply_horizontal_flip(self, image: np.ndarray) -> np.ndarray:
        """Apply random horizontal flip"""
        if np.random.random() < self.config.FLIP_PROBABILITY:
            return cv2.flip(image, 1)
        return image
    
    def _apply_noise(self, image: np.ndarray) -> np.ndarray:
        """Apply random noise"""
        noise = np.random.normal(0, self.config.NOISE_STD, image.shape).astype(np.int16)
        noisy = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return noisy
    
    def _apply_translation(self, image: np.ndarray) -> np.ndarray:
        """Apply random translation (shift)"""
        tx = np.random.randint(*self.config.TRANSLATION_RANGE)
        ty = np.random.randint(*self.config.TRANSLATION_RANGE)
        
        h, w = image.shape[:2]
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        translated = cv2.warpAffine(
            image, translation_matrix, (w, h), borderMode=cv2.BORDER_REFLECT
        )
        
        return translated
    
    def _apply_gaussian_blur(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """Apply slight Gaussian blur"""
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def _apply_sharpening(self, image: np.ndarray) -> np.ndarray:
        """Apply image sharpening"""
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return np.clip(sharpened, 0, 255).astype(np.uint8)
    
    def _apply_histogram_equalization(self, image: np.ndarray) -> np.ndarray:
        """Apply histogram equalization"""
        return cv2.equalizeHist(image)
    
    def get_augmentation_preview(self, face_roi: np.ndarray) -> List[np.ndarray]:
        """
        Generate augmentation preview for visualization
        
        Args:
            face_roi: Original face ROI
            
        Returns:
            List of different augmentations for preview
        """
        previews = [face_roi.copy()]  # Original
        
        # Individual transformations for preview
        previews.append(self._apply_rotation(face_roi.copy()))
        previews.append(self._apply_brightness(face_roi.copy()))
        previews.append(self._apply_contrast(face_roi.copy()))
        previews.append(self._apply_horizontal_flip(face_roi.copy()))
        previews.append(self._apply_noise(face_roi.copy()))
        previews.append(self._apply_translation(face_roi.copy()))
        
        return previews
