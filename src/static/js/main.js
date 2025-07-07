// Face Recognition Demo - Main JavaScript

// Global variables
let video = document.getElementById('video');
let stream = null;
let recognitionInterval = null;
let capturedImageData = null;
let lastDetectedFaces = [];

/**
 * Camera Management Functions
 */
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 }
            } 
        });
        video.srcObject = stream;
        
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('stopBtn').classList.remove('btn-hidden');
        document.getElementById('captureBtn').classList.remove('btn-hidden');
        
        updateStatus('Camera started successfully', 'success');
        
        // Start face recognition
        recognitionInterval = setInterval(recognizeFaces, 1000); // Check every second
        
    } catch (err) {
        console.error('Error accessing camera:', err);
        updateStatus('Error accessing camera: ' + err.message, 'error');
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    if (recognitionInterval) {
        clearInterval(recognitionInterval);
        recognitionInterval = null;
    }
    
    document.getElementById('startBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').classList.add('btn-hidden');
    document.getElementById('captureBtn').classList.add('btn-hidden');
    
    // Clear face overlays
    document.getElementById('face-overlays').innerHTML = '';
    
    // Hide captured photo section and clear data
    document.getElementById('captured-photo-section').classList.add('captured-photo-section');
    capturedImageData = null;
    lastDetectedFaces = [];
    
    // Remove capture overlay if exists
    const overlay = document.querySelector('.capture-overlay');
    if (overlay) {
        overlay.remove();
    }
    
    // Clear detected people info
    displayDetectedPeople([]);
    
    updateStatus('Camera stopped', 'info');
}

/**
 * Face Recognition Functions
 */
async function recognizeFaces() {
    if (!video.videoWidth || !video.videoHeight) return;
    
    try {
        // Capture frame from video
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        // Convert to base64
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        
        // Send to server for recognition
        const response = await fetch('/recognize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayFaces(result.faces);
            lastDetectedFaces = result.detected_people || [];
            updateStatus(`Detected ${result.faces.length} face(s) - Click Capture to save`, 'success');
        } else {
            updateStatus('Recognition error: ' + result.error, 'error');
        }
        
    } catch (err) {
        console.error('Recognition error:', err);
        updateStatus('Recognition error: ' + err.message, 'error');
    }
}

function displayFaces(faces) {
    const overlaysContainer = document.getElementById('face-overlays');
    overlaysContainer.innerHTML = '';
    
    const videoRect = video.getBoundingClientRect();
    const scaleX = videoRect.width / video.videoWidth;
    const scaleY = videoRect.height / video.videoHeight;
    
    faces.forEach(face => {
        const overlay = document.createElement('div');
        overlay.className = 'face-overlay';
        
        const left = face.location.left * scaleX;
        const top = face.location.top * scaleY;
        const width = (face.location.right - face.location.left) * scaleX;
        const height = (face.location.bottom - face.location.top) * scaleY;
        
        overlay.style.left = left + 'px';
        overlay.style.top = top + 'px';
        overlay.style.width = width + 'px';
        overlay.style.height = height + 'px';
        
        // Add label
        const label = document.createElement('div');
        label.className = 'face-label';
        label.textContent = face.name;
        label.style.left = left + 'px';
        label.style.top = top + 'px';
        
        overlaysContainer.appendChild(overlay);
        overlaysContainer.appendChild(label);
    });
}

/**
 * Photo Capture Functions
 */
function capturePhoto() {
    if (!video.videoWidth || !video.videoHeight) {
        updateStatus('Camera not ready for capture', 'error');
        return;
    }

    // Stop recognition temporarily
    if (recognitionInterval) {
        clearInterval(recognitionInterval);
        recognitionInterval = null;
    }

    // Capture frame from video
    const canvas = document.getElementById('capturedCanvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    
    // Draw video frame
    ctx.drawImage(video, 0, 0);
    
    // Draw face overlays on captured image
    const videoRect = video.getBoundingClientRect();
    const scaleX = canvas.width / video.videoWidth;
    const scaleY = canvas.height / video.videoHeight;
    
    // Draw face rectangles and labels on canvas
    const overlays = document.querySelectorAll('.face-overlay, .face-label');
    overlays.forEach(overlay => {
        if (overlay.classList.contains('face-overlay')) {
            const rect = overlay.getBoundingClientRect();
            const videoLeft = videoRect.left;
            const videoTop = videoRect.top;
            
            const x = (rect.left - videoLeft) * scaleX;
            const y = (rect.top - videoTop) * scaleY;
            const width = rect.width * scaleX;
            const height = rect.height * scaleY;
            
            // Draw rectangle
            ctx.strokeStyle = '#4facfe';
            ctx.lineWidth = 3;
            ctx.strokeRect(x, y, width, height);
            
            // Draw semi-transparent background for name
            ctx.fillStyle = 'rgba(79, 172, 254, 0.1)';
            ctx.fillRect(x, y, width, height);
        }
    });
    
    // Draw name labels
    document.querySelectorAll('.face-label').forEach(label => {
        const rect = label.getBoundingClientRect();
        const videoLeft = videoRect.left;
        const videoTop = videoRect.top;
        
        const x = (rect.left - videoLeft) * scaleX;
        const y = (rect.top - videoTop) * scaleY;
        
        // Draw label background
        ctx.fillStyle = '#4facfe';
        ctx.fillRect(x, y - 25, ctx.measureText(label.textContent).width + 20, 25);
        
        // Draw label text
        ctx.fillStyle = 'white';
        ctx.font = '16px Arial';
        ctx.fillText(label.textContent, x + 10, y - 8);
    });
    
    // Store captured image data
    capturedImageData = canvas.toDataURL('image/jpeg', 0.9);
    
    // Show captured photo section
    document.getElementById('captured-photo-section').classList.remove('captured-photo-section');
    
    // Add overlay to video to indicate capture mode
    const videoWrapper = document.querySelector('.video-wrapper');
    let overlay = videoWrapper.querySelector('.capture-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'capture-overlay';
        overlay.textContent = '📷 Photo Captured - Confirm or Cancel';
        videoWrapper.appendChild(overlay);
    }
    
    updateStatus('Photo captured! Confirm to show information or cancel to continue', 'info');
}

function confirmCapture() {
    // Show detected people information
    displayDetectedPeople(lastDetectedFaces);
    
    // Hide captured photo section
    document.getElementById('captured-photo-section').classList.add('captured-photo-section');
    
    // Remove capture overlay
    const overlay = document.querySelector('.capture-overlay');
    if (overlay) {
        overlay.remove();
    }
    
    updateStatus(`Showing information for ${lastDetectedFaces.length} detected person(s)`, 'success');
}

function saveCapture() {
    if (!capturedImageData) {
        updateStatus('No captured image to save', 'error');
        return;
    }

    const now = new Date();
    const filename = `capture_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2,'0')}${now.getDate().toString().padStart(2,'0')}_${now.getHours().toString().padStart(2,'0')}${now.getMinutes().toString().padStart(2,'0')}${now.getSeconds().toString().padStart(2,'0')}.jpg`;

    fetch('/save_capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            image: capturedImageData,
            filename: filename 
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            updateStatus(`Photo saved as ${result.filepath}`, 'success');
        } else {
            updateStatus('Error saving photo: ' + result.error, 'error');
        }
    })
    .catch(err => {
        console.error('Save error:', err);
        updateStatus('Error saving photo: ' + err.message, 'error');
    });
}

function cancelCapture() {
    // Hide captured photo section
    document.getElementById('captured-photo-section').classList.add('captured-photo-section');
    
    // Remove capture overlay
    const overlay = document.querySelector('.capture-overlay');
    if (overlay) {
        overlay.remove();
    }
    
    // Resume recognition
    if (stream && !recognitionInterval) {
        recognitionInterval = setInterval(recognizeFaces, 1000);
    }
    
    // Clear detected people info
    displayDetectedPeople([]);
    
    updateStatus('Capture cancelled - continuing live recognition', 'info');
}

/**
 * People Display Functions
 */
function displayDetectedPeople(detectedPeople) {
    const section = document.getElementById('detected-people-section');
    const tableBody = document.getElementById('personnel-table-body');
    
    if (detectedPeople.length > 0) {
        section.style.display = 'block';
        tableBody.innerHTML = '';
        
        detectedPeople.forEach(person => {
            const info = person.info;
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${info.full_name}</td>
                <td>${info.birth_date || ''}</td>
                <td>${info.rank || ''}</td>
                <td>${info.position || ''}</td>
                <td>${info.unit || ''}</td>
            `;
            
            tableBody.appendChild(row);
        });
    } else {
        section.style.display = 'none';
    }
}

/**
 * Training and Settings Functions
 */
async function loadTrainingInfo() {
    try {
        const response = await fetch('/settings');
        const result = await response.json();
        
        if (result.success) {
            const settings = result.settings;
            document.getElementById('training-status').textContent = 
                settings.is_trained ? '✅ Trained' : '❌ Not trained';
            document.getElementById('confidence-threshold').textContent = settings.confidence_threshold;
        }
    } catch (err) {
        console.error('Error loading training info:', err);
    }
}

async function reloadFaces() {
    try {
        const response = await fetch('/reload_faces', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            updateStatus(result.message, 'success');
            
            // Update known faces list
            const faceList = document.querySelector('.face-list');
            faceList.innerHTML = '';
            
            if (result.known_faces.length > 0) {
                result.known_faces.forEach(name => {
                    const tag = document.createElement('span');
                    tag.className = 'face-tag';
                    tag.textContent = name;
                    faceList.appendChild(tag);
                });
            } else {
                const tag = document.createElement('span');
                tag.className = 'face-tag face-tag-inactive';
                tag.textContent = 'No faces loaded';
                faceList.appendChild(tag);
            }
            
            // Update count
            document.querySelector('.known-faces h3').textContent = `👥 Known Faces (${result.known_faces.length})`;
            
            // Reload training info
            loadTrainingInfo();
            
        } else {
            updateStatus('Error reloading faces', 'error');
        }
        
    } catch (err) {
        console.error('Reload error:', err);
        updateStatus('Error reloading faces: ' + err.message, 'error');
    }
}

/**
 * Image Upload Functions
 */
function uploadImage() {
    const input = document.getElementById('uploadInput');
    const status = document.getElementById('upload-status');
    const preview = document.getElementById('upload-preview');
    const previewImg = document.getElementById('upload-preview-img');
    const faceOverlays = document.getElementById('upload-face-overlays');
    
    if (input.files && input.files[0]) {
        const file = input.files[0];
        
        // Show upload status
        status.classList.remove('hidden');
        status.textContent = 'Processing image...';
        status.className = 'status info';
        
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('file', file);
        
        // Send image to server for processing
        fetch('/upload_test', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                status.textContent = `Image processed successfully! Found ${result.faces.length} face(s)`;
                status.className = 'status success';
                
                // Set preview image from server response
                previewImg.src = result.image_base64;
                preview.classList.remove('hidden');
                
                // Clear previous overlays
                faceOverlays.innerHTML = '';
                
                // Display detected faces on uploaded image
                if (result.faces && result.faces.length > 0) {
                    result.faces.forEach(face => {
                        const overlay = document.createElement('div');
                        overlay.className = 'upload-overlay';
                        overlay.style.left = face.location.left + 'px';
                        overlay.style.top = face.location.top + 'px';
                        overlay.style.width = (face.location.right - face.location.left) + 'px';
                        overlay.style.height = (face.location.bottom - face.location.top) + 'px';
                        
                        const label = document.createElement('div');
                        label.className = 'upload-label';
                        label.textContent = face.name;
                        overlay.appendChild(label);
                        
                        faceOverlays.appendChild(overlay);
                    });
                }
                
                // Display detected people information
                if (result.detected_people && result.detected_people.length > 0) {
                    displayDetectedPeople(result.detected_people);
                }
                
            } else {
                status.textContent = 'Error processing image: ' + result.error;
                status.className = 'status error';
            }
        })
        .catch(err => {
            console.error('Upload error:', err);
            status.textContent = 'Error uploading image: ' + err.message;
            status.className = 'status error';
        });
    }
}

/**
 * Utility Functions
 */
function updateStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status ${type}`;
}

/**
 * Event Listeners
 */
// Load training info on page load
window.addEventListener('load', loadTrainingInfo);

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});

// Initialize video element when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    video = document.getElementById('video');
});
