# Installation Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Webcam or camera device
- 4GB RAM minimum, 8GB recommended
- 2GB free disk space

### Operating Systems
- Windows 10/11
- macOS 10.14+
- Ubuntu 18.04+ or other Linux distributions

## Installation Methods

### Method 1: Local Installation

#### 1. Clone or Download Project
```bash
git clone <repository-url>
cd face-recognition-demo
```

#### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Prepare Dataset
```bash
# Create dataset directory structure
mkdir -p dataset
mkdir -p captures
mkdir -p logs

# Add your training images to dataset/PersonName/ folders
# Example:
# dataset/
#   ├── John_Doe/
#   │   ├── john1.jpg
#   │   ├── john2.jpg
#   └── Jane_Smith/
#       ├── jane1.jpg
#       └── jane2.jpg
```

#### 5. Run Application
```bash
python app_new.py
```

Open browser and navigate to: http://localhost:5000

### Method 2: Docker Installation

#### 1. Install Docker
- Download and install Docker Desktop from https://docker.com
- Ensure Docker is running

#### 2. Build and Run with Docker
```bash
# Build image
docker build -t face-recognition .

# Run container
docker run -p 5000:5000 \
  -v $(pwd)/dataset:/app/dataset \
  -v $(pwd)/captures:/app/captures \
  face-recognition
```

#### 3. Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Configuration

### 1. People Information Setup
Edit `people_info.json` to add person details:
```json
{
  "Person_Name": {
    "full_name": "Full Display Name",
    "position": "Job Title",
    "department": "Department Name",
    "email": "email@company.com",
    "phone": "+1 234 567 8900",
    "bio": "Brief biography or description"
  }
}
```

### 2. System Settings
Edit `config/settings.py` to customize:
- Confidence threshold
- Data augmentation settings
- File paths
- Flask configuration

### 3. Training Dataset
For best results:
- Use 3-5 clear photos per person
- Include different angles and lighting
- Ensure faces are clearly visible
- Use good quality images (not blurry)

## Troubleshooting

### Common Issues

#### OpenCV Installation Problems
```bash
# If OpenCV fails to install
pip uninstall opencv-python
pip install opencv-python-headless

# For full OpenCV with GUI support
pip install opencv-contrib-python
```

#### Camera Access Issues
- Windows: Check camera permissions in Settings > Privacy & Security > Camera
- macOS: Grant camera access in System Preferences > Security & Privacy > Camera
- Linux: Ensure user is in `video` group
  ```bash
  sudo usermod -a -G video $USER
  ```

#### Memory Issues
- Reduce image size in dataset
- Disable data augmentation temporarily
- Close other applications
- Increase virtual memory/swap

#### Import Errors
```bash
# Ensure all dependencies are installed
pip install --upgrade -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Performance Optimization

#### For Better Recognition Accuracy
1. Use high-quality training images
2. Include multiple angles per person
3. Ensure good lighting conditions
4. Enable data augmentation
5. Adjust confidence threshold

#### For Better Performance
1. Resize large images in dataset
2. Reduce recognition frequency
3. Disable debug mode in production
4. Use production WSGI server

### Development Setup

#### Additional Tools for Development
```bash
# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest tests/

# Code formatting
black src/

# Linting
flake8 src/

# Type checking
mypy src/
```

#### IDE Setup
- VS Code: Install Python extension
- PyCharm: Configure Python interpreter
- Jupyter: For interactive development
  ```bash
  pip install jupyter
  jupyter notebook
  ```

## Production Deployment

### Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.app_factory:create_app()"
```

### Using uWSGI
```bash
pip install uwsgi
uwsgi --http :5000 --module src.app_factory:create_app()
```

### Environment Variables
```bash
export FLASK_ENV=production
export DEBUG=False
export HOST=0.0.0.0
export PORT=5000
export SECRET_KEY=your-secret-key-here
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Support

### Getting Help
1. Check this documentation
2. Review error logs in `logs/` directory
3. Check GitHub Issues
4. Contact development team

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes and test
4. Submit pull request

### License
This project is licensed under the MIT License - see LICENSE file for details.
