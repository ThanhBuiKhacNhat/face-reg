"""
Flask API Routes for Face Recognition System
"""
import os
import cv2
import numpy as np
import base64
import time
from io import BytesIO
from PIL import Image
from flask import Blueprint, request, jsonify, current_app
import logging

logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/recognize', methods=['POST'])
def recognize():
    """Face recognition from camera stream"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data provided'})
        
        # Get models from app context
        face_model = current_app.face_model
        people_manager = current_app.people_manager
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'success': False, 'error': 'Invalid image data'})
        
        # Perform face recognition
        face_locations, face_names = face_model.recognize_faces(frame)
        
        # Prepare response data
        faces = []
        detected_people = []
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            faces.append({
                'name': name,
                'location': {
                    'top': int(top), 
                    'right': int(right), 
                    'bottom': int(bottom), 
                    'left': int(left)
                }
            })
            
            if name != "Unknown":
                person_info = people_manager.get_person_info(name)
                detected_people.append({
                    'name': name,
                    'info': person_info
                })
        
        return jsonify({
            'success': True,
            'faces': faces,
            'detected_people': detected_people
        })
        
    except Exception as e:
        logger.error(f"Recognition error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/upload_test', methods=['POST'])
def upload_test():
    """Process uploaded image for face recognition testing"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        # Get models from app context
        face_model = current_app.face_model
        people_manager = current_app.people_manager
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Read and process image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'success': False, 'error': 'Invalid image file'})
        
        # Convert back to base64 for display
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode()}"
        
        # Perform face recognition
        face_locations, face_names = face_model.recognize_faces(frame)
        
        # Prepare response data
        faces = []
        detected_people = []
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            faces.append({
                'name': name,
                'location': {
                    'top': int(top), 
                    'right': int(right), 
                    'bottom': int(bottom), 
                    'left': int(left)
                }
            })
            
            if name != "Unknown":
                person_info = people_manager.get_person_info(name)
                detected_people.append({
                    'name': name,
                    'info': person_info
                })
        
        return jsonify({
            'success': True,
            'faces': faces,
            'detected_people': detected_people,
            'image_base64': image_base64
        })
        
    except Exception as e:
        logger.error(f"Upload test error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/save_capture', methods=['POST'])
def save_capture():
    """Save captured photo"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data provided'})
        
        # Import config here to avoid circular imports
        from config.settings import StorageConfig
        config = StorageConfig()
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Create captures directory if it doesn't exist
        captures_dir = config.CAPTURES_PATH
        os.makedirs(captures_dir, exist_ok=True)
        
        # Generate filename
        filename = data.get('filename', f'capture_{int(time.time())}.jpg')
        filepath = os.path.join(captures_dir, filename)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        return jsonify({
            'success': True,
            'filepath': filename,
            'full_path': filepath
        })
        
    except Exception as e:
        logger.error(f"Save capture error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/reload_faces', methods=['POST'])
def reload_faces():
    """Reload and retrain face recognition model"""
    try:
        # Get models from app context
        face_model = current_app.face_model
        people_manager = current_app.people_manager
        
        # Reload people info
        people_manager.load_people_info()
        
        # Import config here to avoid circular imports
        from config.settings import StorageConfig
        config = StorageConfig()
        
        # Retrain model
        result = face_model.train(str(config.DATASET_PATH))
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Reloaded {len(face_model.known_face_names)} faces',
                'known_faces': face_model.known_face_names,
                'training_info': result.get('training_info', {})
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Training failed')
            })
        
    except Exception as e:
        logger.error(f"Reload faces error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/people_info')
def people_info():
    """Get information about all people"""
    try:
        # Get people manager from app context
        people_manager = current_app.people_manager
        
        return jsonify({
            'success': True,
            'people': people_manager.get_all_people(),
            'count': len(people_manager.people_info)
        })
        
    except Exception as e:
        logger.error(f"People info error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/settings')
def settings():
    """Get current system settings and training status"""
    try:
        # Get face model from app context
        face_model = current_app.face_model
        
        return jsonify({
            'success': True,
            'settings': {
                'is_trained': face_model.is_trained,
                'confidence_threshold': face_model.confidence_threshold,
                'known_faces_count': len(face_model.known_face_names),
                'use_augmentation': face_model.use_augmentation,
                'augmentation_factor': face_model.augmentation_factor
            }
        })
        
    except Exception as e:
        logger.error(f"Settings error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/update_settings', methods=['POST'])
def update_settings():
    """Update system settings"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        # Get face model from app context
        face_model = current_app.face_model
        
        # Update settings
        if 'confidence_threshold' in data:
            face_model.confidence_threshold = float(data['confidence_threshold'])
        
        if 'use_augmentation' in data:
            face_model.use_augmentation = bool(data['use_augmentation'])
        
        if 'augmentation_factor' in data:
            face_model.augmentation_factor = int(data['augmentation_factor'])
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully',
            'settings': {
                'confidence_threshold': face_model.confidence_threshold,
                'use_augmentation': face_model.use_augmentation,
                'augmentation_factor': face_model.augmentation_factor
            }
        })
        
    except Exception as e:
        logger.error(f"Update settings error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/training_status')
def training_status():
    """Get detailed training status and quality information"""
    try:
        # Get models from app context
        face_model = current_app.face_model
        people_manager = current_app.people_manager
        
        # Get training info
        training_info = face_model.get_training_summary()
        
        return jsonify({
            'success': True,
            'training_status': {
                'is_trained': face_model.is_trained,
                'total_people': len(face_model.known_face_names),
                'confidence_threshold': face_model.confidence_threshold,
                'training_info': training_info
            }
        })
        
    except Exception as e:
        logger.error(f"Training status error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Get models from app context
        face_model = current_app.face_model
        people_manager = current_app.people_manager
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'components': {
                'face_model': 'ok' if face_model else 'error',
                'people_manager': 'ok' if people_manager else 'error',
                'is_trained': face_model.is_trained if face_model else False
            }
        })
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
