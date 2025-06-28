# 🤖 Multimodal AI Assistant

A Tkinter-based application that runs three AI models simultaneously for gesture control, speech recognition, and object detection.

## 🚀 Features

### 1. 👋 Gesture Recognition
- **Volume Control**: Thumb up/down gestures to control system volume
- **Brightness Control**: Index finger up/down gestures to control screen brightness
- **Mouse Control**: Open palm gesture for mouse movement
- **Screenshot**: Peace sign gesture to take screenshots

### 2. 🎤 Speech Recognition
- **Voice Commands**: Control system functions with voice
- **Supported Commands**:
  - "Volume up/down" or "Increase/decrease volume"
  - "Mute" or "Unmute"
  - "Brightness up/down" or "Increase/decrease brightness"
  - "Screenshot" or "Take screenshot"
  - "Open notepad" or "Open calculator"
  - "Close" or "Exit"

### 3. 👁️ Object Detection
- **Real-time Detection**: Detects objects using YOLOv8
- **Multiple Objects**: Recognizes 80+ different object classes
- **Confidence Display**: Shows detection confidence levels

## 📋 Requirements

- Python 3.8+
- Webcam
- Microphone
- Windows 10/11 (for system controls)

## 🛠️ Installation

1. **Clone or download the project**
2. **Navigate to the project directory**:
   ```bash
   cd multimodal_app
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLO model** (will be downloaded automatically on first run):
   ```bash
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
   ```

## 🎯 Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Start all models** by clicking the "🚀 Start All Models" button

3. **Use the features**:
   - **Gestures**: Show hand gestures to the camera
   - **Voice**: Speak commands clearly into the microphone
   - **Objects**: Point camera at objects to detect them

## 🎮 Gesture Guide

### Volume Control
- **Volume Up**: Thumb pointing up, other fingers closed
- **Volume Down**: Thumb pointing down, other fingers closed

### Brightness Control
- **Brightness Up**: Index finger pointing up, other fingers closed
- **Brightness Down**: Index finger pointing down, other fingers closed

### Mouse Control
- **Mouse Movement**: Open palm (all fingers extended)

### Screenshot
- **Take Screenshot**: Peace sign (index and middle fingers extended)

## 🎤 Voice Commands

| Command | Action |
|---------|--------|
| "Volume up" | Increase system volume |
| "Volume down" | Decrease system volume |
| "Mute" | Toggle mute |
| "Brightness up" | Increase screen brightness |
| "Brightness down" | Decrease screen brightness |
| "Screenshot" | Take a screenshot |
| "Open notepad" | Launch Notepad |
| "Open calculator" | Launch Calculator |
| "Close" | Exit the application |

## 🔧 Troubleshooting

### Common Issues

1. **Camera not working**:
   - Ensure webcam is connected and not in use by other applications
   - Check camera permissions in Windows settings

2. **Microphone not working**:
   - Ensure microphone is connected and set as default
   - Check microphone permissions in Windows settings

3. **Models not loading**:
   - Ensure all dependencies are installed correctly
   - Check internet connection for YOLO model download

4. **Performance issues**:
   - Close other applications using camera/microphone
   - Reduce camera resolution if needed
   - Ensure adequate lighting for gesture recognition

### Error Messages

- **"Cannot open camera"**: Check camera connection and permissions
- **"Speech recognition error"**: Check microphone and internet connection
- **"Model initialization error"**: Reinstall dependencies

## 📁 Project Structure

```
multimodal_app/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🛡️ Safety Notes

- **System Controls**: The app can control volume, brightness, and take screenshots
- **Privacy**: Camera and microphone data is processed locally
- **Permissions**: Grant camera and microphone permissions when prompted

## 🔄 Updates

- **Gesture Recognition**: Uses MediaPipe for real-time hand tracking
- **Speech Recognition**: Uses Google Speech Recognition API
- **Object Detection**: Uses YOLOv8 for real-time object detection

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify camera and microphone permissions
4. Check system requirements

## 🎉 Enjoy!

The Multimodal AI Assistant provides an intuitive way to interact with your computer using gestures, voice, and visual recognition. Experiment with different gestures and voice commands to discover all the features! 