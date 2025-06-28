# Speech-to-Text Functionality Guide

## Overview

The multimodal app now includes improved speech-to-text functionality that displays transcribed text in real-time below the camera feed. This feature works in parallel with gesture recognition and object detection using **Google Speech Recognition API**.

## Features

### 🎤 Real-time Speech Transcription
- **Live Display**: Transcribed text appears immediately below the camera feed
- **Parallel Processing**: Works simultaneously with other features
- **Google Speech Recognition**: Uses Google's reliable speech recognition service
- **Voice Commands**: Supports various voice commands for system control

### 📱 Voice Commands Supported
- **Volume Control**: "volume up", "volume down", "mute"
- **Brightness Control**: "brightness up", "brightness down"
- **Screenshots**: "take screenshot", "screenshot"
- **Applications**: "open notepad", "open calculator"
- **System**: "close", "exit"

## Installation

### Required Dependencies
```bash
pip install -r requirements.txt
```

### Speech Recognition Setup
The app uses Google Speech Recognition API which requires:
- Internet connection
- Microphone access
- Google Speech Recognition service (free tier available)

## Usage

### Starting the Application
```bash
python main.py
```

### Using Speech-to-Text
1. Click "🚀 Start All Models" to begin
2. Speak clearly into your microphone
3. Watch the transcribed text appear in the "Live Speech Transcription" area
4. Use voice commands to control your system

### Testing Speech Recognition
Run the test script to verify your setup:
```bash
python test_speech.py
```

## Technical Details

### Speech Recognition Method

#### Google Speech Recognition
- **Service**: Google's speech recognition API
- **Accuracy**: High accuracy with noise reduction
- **Processing**: Real-time audio processing
- **Requirements**: Internet connection
- **Cost**: Free tier available

### Audio Processing
- **Sample Rate**: 16kHz (standard for speech recognition)
- **Channels**: Mono (1 channel)
- **Processing**: Real-time audio capture and processing
- **Noise Reduction**: Automatic ambient noise adjustment

## Troubleshooting

### Common Issues

#### 1. "No speech detected"
- **Solution**: Check microphone permissions
- **Test**: Run `python test_speech.py`

#### 2. "Speech recognition service error"
- **Solution**: Check internet connection
- **Alternative**: Verify Google Speech Recognition service is accessible

#### 3. "Audio device error"
- **Solution**: Check microphone connection
- **Test**: Verify in system sound settings

#### 4. "Could not understand audio"
- **Solution**: Speak more clearly and reduce background noise
- **Alternative**: Check microphone quality and positioning

### Performance Tips

1. **Microphone Quality**: Use a good quality microphone for better accuracy
2. **Environment**: Reduce background noise
3. **Speaking**: Speak clearly and at normal volume
4. **Distance**: Keep microphone at consistent distance
5. **Internet**: Ensure stable internet connection for Google API

### System Requirements

#### Minimum
- Python 3.8+
- 4GB RAM
- Microphone
- Internet connection (for Google Speech Recognition)

#### Recommended
- Python 3.9+
- 8GB RAM
- USB microphone
- Stable internet connection

## Advanced Configuration

### Customizing Voice Commands
Edit the `process_voice_command` method in `main.py` to add new commands:

```python
elif "your command" in command:
    # Your custom action here
    self.log_message("Custom action executed")
```

### Adjusting Audio Settings
Modify these parameters in the `__init__` method:
- `self.sample_rate = 16000` - Audio sample rate
- Timeout and phrase time limits in `_listen_for_audio` method
- Ambient noise adjustment duration

### Speech Recognition Parameters
Adjust recognition parameters in `_listen_for_audio`:
```python
return self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
```

## File Structure

```
multimodal_app/
├── main.py                 # Main application
├── test_speech.py          # Speech recognition test
├── requirements.txt        # Dependencies
├── SPEECH_TO_TEXT_GUIDE.md # This guide
└── yolov8n.pt             # YOLO model
```

## Support

If you encounter issues:
1. Run `python test_speech.py` to diagnose problems
2. Check microphone permissions
3. Verify internet connection
4. Try reinstalling dependencies

## Future Enhancements

- [ ] Offline speech recognition options
- [ ] Multiple language support
- [ ] Custom wake word detection
- [ ] Voice activity detection improvements
- [ ] Integration with more system controls
- [ ] Alternative speech recognition services 