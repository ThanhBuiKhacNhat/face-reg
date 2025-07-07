# 🔍 Face Recognition Web Application

A professional Computer Vision application for real-time face recognition using OpenCV and Flask. Supports 5-10 people recognition with modern web interface, data augmentation, and comprehensive management features.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **Real-time Face Recognition**: Live camera feed with instant face detection and recognition
- **Web-based Interface**: Modern, responsive UI accessible from any browser
- **Multi-person Support**: Recognize 5-10 people simultaneously
- **Data Augmentation**: Advanced image augmentation for better training accuracy
- **Upload Testing**: Test recognition with uploaded images
- **Capture & Save**: Save photos with detection results
- **Person Management**: Comprehensive person information system
- **Professional Architecture**: Modular, scalable codebase following best practices

## 🏗️ Project Structure

```
face-recognition-demo/
├── 📁 src/                          # Source code modules
│   ├── 📁 api/                      # Flask API routes
│   │   ├── __init__.py
│   │   └── routes.py                # REST API endpoints
│   ├── 📁 models/                   # ML models
│   │   ├── __init__.py
│   │   └── face_recognition_model.py # LBPH face recognition
│   ├── 📁 utils/                    # Utility modules
│   │   ├── __init__.py
│   │   ├── image_processor.py       # Image processing utilities
│   │   ├── augmentation.py          # Data augmentation
│   │   └── people_manager.py        # Person info management
│   ├── 📁 static/                   # Static web assets
│   │   ├── css/                     # Stylesheets
│   │   └── js/                      # JavaScript files
│   ├── 📁 templates/                # HTML templates
│   │   └── index.html               # Main interface
│   ├── __init__.py
│   └── app_factory.py               # Flask application factory
├── 📁 config/                       # Configuration files
│   ├── __init__.py
│   └── settings.py                  # System configuration
├── 📁 dataset/                      # Training images
│   ├── Person1/                     # One folder per person
│   ├── Person2/
│   └── ...
├── 📁 captures/                     # Saved captures
├── 📁 logs/                         # Application logs
├── 📁 docs/                         # Documentation
│   ├── API.md                       # API documentation
│   └── INSTALLATION.md              # Setup guide
├── 📁 tests/                        # Unit tests
│   └── test_face_recognition.py
├── app_new.py                       # Main application entry point
├── people_info.json                 # Person information database
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── docker-compose.yml               # Docker Compose setup
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## 🚀 Quick Start

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd face-recognition-demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare dataset**
   ```bash
   # Create dataset structure
   mkdir -p dataset/Person1 dataset/Person2
   
   # Add training images to respective folders
   # dataset/Person1/photo1.jpg, photo2.jpg, ...
   # dataset/Person2/photo1.jpg, photo2.jpg, ...
   ```

4. **Run the application**
   ```bash
   python app_new.py
   ```

5. **Open browser**
   Navigate to: http://localhost:5000

### Option 2: Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t face-recognition .
docker run -p 5000:5000 face-recognition
```

## 📋 Requirements

- Python 3.8+
- OpenCV 4.0+
- Flask 2.0+
- Webcam/Camera device
- 4GB RAM (8GB recommended)

## 🔧 Configuration

### Dataset Setup
1. Create folders in `dataset/` for each person
2. Add 3-5 clear photos per person
3. Run the application to auto-generate `people_info.json`
4. Edit `people_info.json` to add detailed person information

### System Settings
Edit `config/settings.py` to customize:
- Confidence threshold
- Data augmentation parameters
- File paths and directories
- Flask configuration

## 🎯 Usage

### Training
1. **Prepare Dataset**: Add training images to `dataset/PersonName/` folders
2. **Auto-Training**: Model trains automatically when you start the app
3. **Manual Reload**: Click "Reload Faces" button to retrain

### Recognition
1. **Start Camera**: Click "Start Camera" button
2. **Real-time Detection**: Faces are detected and recognized automatically
3. **Capture Photos**: Save detection results for documentation
4. **Upload Testing**: Test with uploaded images

### Person Management
- Edit `people_info.json` to add person details
- Includes name, position, contact info, biography
- Supports avatar images

## 🧪 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/recognize` | POST | Real-time face recognition |
| `/upload_test` | POST | Test with uploaded image |
| `/reload_faces` | POST | Retrain the model |
| `/save_capture` | POST | Save captured photo |
| `/settings` | GET | Get system settings |

See [API Documentation](docs/API.md) for detailed information.

## 🏛️ Architecture

### Core Components
- **FaceRecognitionModel**: LBPH-based face recognition engine
- **ImageProcessor**: Image preprocessing and face extraction
- **DataAugmentation**: Training data enhancement
- **PeopleManager**: Person information management
- **API Routes**: RESTful web services

### Technology Stack
- **Backend**: Python, Flask, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Algorithm**: LBPH (Local Binary Pattern Histogram)
- **Storage**: File-based (JSON, images)
- **Deployment**: Docker, Docker Compose

## 🔬 Advanced Features

### Data Augmentation
- **Rotation**: ±15 degrees
- **Brightness**: 70-130% variation
- **Contrast**: 80-120% adjustment
- **Horizontal Flip**: 50% probability
- **Noise Addition**: Gaussian noise
- **Translation**: ±5 pixel shifts

### Training Quality
- **Automatic Assessment**: Star rating system (⭐⭐⭐)
- **Quality Metrics**: Based on number of training images
- **Recommendations**: Guidance for improving accuracy

## 🐳 Docker Support

### Development
```bash
docker-compose up -d
```

### Production
```bash
docker build -t face-recognition:prod .
docker run -d -p 80:5000 \
  --name face-recognition \
  --restart unless-stopped \
  face-recognition:prod
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific test file
pytest tests/test_face_recognition.py
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.app_factory:create_app()"
```

### Environment Variables
```bash
export FLASK_ENV=production
export DEBUG=False
export SECRET_KEY=your-secret-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation
- Use type hints
- Add logging for debugging

## 🔒 Security Considerations

- Change default secret key in production
- Implement proper authentication for production use
- Validate all file uploads
- Sanitize user inputs
- Use HTTPS in production

## 📊 Performance Tips

- Use smaller training images for faster processing
- Adjust recognition frequency based on needs
- Enable data augmentation for better accuracy
- Monitor memory usage with large datasets

## 🐛 Troubleshooting

### Common Issues
1. **Camera not detected**: Check permissions and device connections
2. **Import errors**: Ensure all dependencies are installed
3. **Memory issues**: Reduce image sizes or close other applications
4. **Poor recognition**: Add more training images or adjust confidence threshold

See [Installation Guide](docs/INSTALLATION.md) for detailed troubleshooting.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Face Recognition Team** - Initial development

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Flask team for the web framework
- Contributors and testers

## 📞 Support

- 📖 [Documentation](docs/)
- 🐛 [Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

---

**Made with ❤️ for Computer Vision and AI**
