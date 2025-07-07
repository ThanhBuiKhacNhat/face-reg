# Face Recognition System API Documentation

## Overview
This document describes the REST API endpoints for the Face Recognition System.

## Base URL
```
http://localhost:5000
```

## Authentication
No authentication required for this demo version.

## Endpoints

### 1. Home Page
**GET /** 
- **Description**: Serves the main web interface
- **Response**: HTML page with face recognition interface

### 2. Face Recognition
**POST /recognize**
- **Description**: Recognizes faces in a provided image from camera stream
- **Content-Type**: application/json
- **Request Body**:
  ```json
  {
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "faces": [
      {
        "name": "Lê Hồ Mạnh Thắng",
        "confidence": 45.2,
        "location": {
          "left": 100,
          "top": 50,
          "right": 200,
          "bottom": 150
        }
      }
    ],
    "detected_people": [
      {
        "name": "Lê Hồ Mạnh Thắng",
        "info": {
          "full_name": "Lê Hồ Mạnh Thắng",
          "position": "Software Engineer",
          "department": "AI/ML",
          "email": "thang.le@company.com",
          "phone": "+84 123 456 789",
          "bio": "Expert in Computer Vision and AI"
        }
      }
    ]
  }
  ```

### 3. Upload Test Image
**POST /upload_test**
- **Description**: Tests face recognition on uploaded image file
- **Content-Type**: multipart/form-data
- **Request**: File upload with key "file"
- **Response**: Same as /recognize endpoint plus processed image

### 4. Reload Faces
**POST /reload_faces**
- **Description**: Retrains the model with current dataset
- **Response**:
  ```json
  {
    "success": true,
    "message": "Faces reloaded successfully. Trained on 9 people with 45 images.",
    "known_faces": ["Person1", "Person2", "..."]
  }
  ```

### 5. Save Capture
**POST /save_capture**
- **Description**: Saves a captured photo with detections
- **Request Body**:
  ```json
  {
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "filename": "capture_20250706_123456.jpg"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "filepath": "captures/capture_20250706_123456.jpg"
  }
  ```

### 6. Get Settings
**GET /settings**
- **Description**: Returns current system settings and training status
- **Response**:
  ```json
  {
    "success": true,
    "settings": {
      "is_trained": true,
      "confidence_threshold": 100,
      "use_augmentation": true,
      "augmentation_factor": 2,
      "total_people": 9,
      "total_images": 45
    }
  }
  ```

## Error Responses
All endpoints return error responses in this format:
```json
{
  "success": false,
  "error": "Error description",
  "details": "Additional error details (optional)"
}
```

## Status Codes
- **200**: Success
- **400**: Bad Request (invalid input)
- **500**: Internal Server Error

## Data Formats

### Face Location
```json
{
  "left": 100,    // X coordinate of left edge
  "top": 50,      // Y coordinate of top edge  
  "right": 200,   // X coordinate of right edge
  "bottom": 150   // Y coordinate of bottom edge
}
```

### Person Information
```json
{
  "full_name": "Full Name",
  "position": "Job Title",
  "department": "Department Name", 
  "email": "email@company.com",
  "phone": "+84 123 456 789",
  "bio": "Brief biography",
  "avatar": "path/to/avatar.jpg" // Optional
}
```

## Usage Examples

### JavaScript (Fetch API)
```javascript
// Recognize faces from canvas
const canvas = document.getElementById('video-canvas');
const imageData = canvas.toDataURL('image/jpeg', 0.8);

fetch('/recognize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image: imageData })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('Found faces:', data.faces);
  }
});

// Upload image file
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/upload_test', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python (Requests)
```python
import requests
import base64

# Recognize faces
with open('test_image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post('http://localhost:5000/recognize', 
                        json={'image': f'data:image/jpeg;base64,{image_data}'})
print(response.json())

# Upload file
with open('test_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/upload_test', files=files)
    print(response.json())
```

## Configuration

### Dataset Structure
```
dataset/
├── Person1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Person2/
│   ├── image1.jpg
│   └── ...
└── people_info.json  # Person information config
```

### People Info Format
```json
{
  "Person Name": {
    "full_name": "Full Display Name",
    "position": "Job Title",
    "department": "Department",
    "email": "email@company.com", 
    "phone": "Phone Number",
    "bio": "Biography text",
    "avatar": "path/to/avatar.jpg"
  }
}
```
