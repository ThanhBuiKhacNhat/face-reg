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
        """Process image from webcam and return recognition results"""
        try:
            # Get image data from request
            data = request.get_json()
            image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert PIL image to OpenCV format
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Recognize faces
            face_locations, face_names = face_model.recognize_faces(frame)
            
            # Prepare response
            faces = []
            detected_people = []
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                face_info = {
                    'name': name,
                    'location': {
                        'top': int(top),
                        'right': int(right),
                        'bottom': int(bottom),
                        'left': int(left)
                    }
                }
                faces.append(face_info)
                
                # Get detailed person information
                person_info = people_manager.get_person_info(name)
                if name not in [p['name'] for p in detected_people]:
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
            logger.error(f"Recognition error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @api.route('/upload_test', methods=['POST'])
    def upload_test():
        """Upload and test face recognition on an image"""
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file uploaded'
                })
            
            file = request.files['file']
            
            # Check if file is selected
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                })
            
            # Check file type
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            if not ('.' in file.filename and 
                    file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                return jsonify({
                    'success': False,
                    'error': 'Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.'
                })
            
            # Read image from memory
            file_bytes = file.read()
            
            # Convert to OpenCV format
            nparr = np.frombuffer(file_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return jsonify({
                    'success': False,
                    'error': 'Could not read image file'
                })
            
            # Recognize faces in the uploaded image
            face_locations, face_names = face_model.recognize_faces(frame)
            
            # Prepare response
            faces = []
            detected_people = []
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                face_info = {
                    'name': name,
                    'location': {
                        'top': int(top),
                        'right': int(right),
                        'bottom': int(bottom),
                        'left': int(left)
                    }
                }
                faces.append(face_info)
                
                # Get detailed person info if recognized
                if name != "Unknown":
                    person_info = people_manager.get_person_info(name)
                    detected_people.append({
                        'name': name,
                        'info': person_info
                    })
            
            # Convert image back to base64 for display
            _, buffer = cv2.imencode('.jpg', frame)
            image_base64 = base64.b64encode(buffer).decode()
            
            return jsonify({
                'success': True,
                'faces': faces,
                'detected_people': detected_people,
                'image_base64': f'data:image/jpeg;base64,{image_base64}',
                'filename': file.filename
            })
        
        except Exception as e:
            logger.error(f"Upload test error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @api.route('/reload_faces', methods=['POST'])
    def reload_faces():
        """Reload known faces from dataset"""
        try:
            # Reload people info
            people_manager.load_people_info()
            
            # Retrain model
            from ..config.settings import StorageConfig
            config = StorageConfig()
            result = face_model.train(str(config.DATASET_PATH))
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': f'Reloaded {len(face_model.known_face_names)} faces',
                    'known_faces': face_model.known_face_names,
                    'training_stats': result.get('stats', {})
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Training failed')
                })
                
        except Exception as e:
            logger.error(f"Reload faces error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @api.route('/people_info')
    def get_people_info():
        """Get all people information"""
        return jsonify({
            'success': True,
            'people': people_manager.get_all_people(),
            'statistics': people_manager.get_statistics()
        })
    
    @api.route('/people_info/<name>', methods=['GET'])
    def get_person_info_by_name(name):
        """Get information for a specific person"""
        info = people_manager.get_person_info(name)
        return jsonify({
            'success': True,
            'person': info
        })
    
    @api.route('/people_info/<name>', methods=['POST'])
    def update_person_info(name):
        """Update information for a specific person"""
        try:
            data = request.get_json()
            success = people_manager.update_person(name, data)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': f'Updated information for {name}'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to update person information'
                })
        except Exception as e:
            logger.error(f"Update person error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @api.route('/save_capture', methods=['POST'])
    def save_capture():
        """Save captured photo with detection results"""
        try:
            data = request.get_json()
            image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
            filename = data.get('filename', f'capture_{int(time.time())}.jpg')
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Create captures directory if it doesn't exist
            from ..config.settings import StorageConfig
            config = StorageConfig()
            config.ensure_directories()
            
            # Save image
            filepath = config.CAPTURES_PATH / filename
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            return jsonify({
                'success': True,
                'message': f'Capture saved as {filename}',
                'filepath': str(filepath)
            })
        
        except Exception as e:
            logger.error(f"Save capture error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @api.route('/settings', methods=['GET', 'POST'])
    def settings():
        """Get or update recognition settings"""
        if request.method == 'GET':
            model_info = face_model.get_model_info()
            return jsonify({
                'success': True,
                'settings': {
                    'confidence_threshold': model_info['confidence_threshold'],
                    'is_trained': model_info['is_trained'],
                    'total_people': model_info['total_people'],
                    'use_augmentation': model_info['config']['use_augmentation'],
                    'augmentation_factor': model_info['config']['augmentation_factor'],
                    'training_stats': model_info.get('training_stats', {})
                }
            })
        else:
            try:
                data = request.get_json()
                settings_changed = False
                
                # Update model configuration
                config_updates = {}
                for key in ['confidence_threshold', 'use_augmentation', 'augmentation_factor']:
                    if key in data:
                        config_updates[key] = data[key]
                        settings_changed = True
                
                if config_updates:
                    face_model.update_config(**config_updates)
                
                message = 'Settings updated successfully'
                if settings_changed and ('use_augmentation' in data or 'augmentation_factor' in data):
                    message += '. Consider reloading faces to apply augmentation changes.'
                
                return jsonify({
                    'success': True,
                    'message': message
                })
            except Exception as e:
                logger.error(f"Settings update error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
    
    @api.route('/model_info')
    def model_info():
        """Get detailed model information"""
        try:
            info = face_model.get_model_info()
            return jsonify({
                'success': True,
                'model_info': info
            })
        except Exception as e:
            logger.error(f"Model info error: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    return api
