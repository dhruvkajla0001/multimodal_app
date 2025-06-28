# Speech-to-Text Functionality Guide

## Overview

The multimodal app now includes improved speech-to-text functionality that displays transcribed text in real-time below the camera feed. This feature works in parallel with gesture recognition and object detection.

## Features

### 🎤 Real-time Speech Transcription
- **Live Display**: Transcribed text appears immediately below the camera feed
- **Parallel Processing**: Works simultaneously with other features
- **Fallback Support**: Uses traditional speech recognition if advanced features aren't available
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

### Optional: Enhanced Speech Recognition
For better accuracy, install Whisper:
```bash
pip install openai-whisper
```

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

### Speech Recognition Methods

#### 1. Whisper (Recommended)
- **Model**: OpenAI Whisper "base" model
- **Accuracy**: High accuracy with noise reduction
- **Processing**: Real-time audio streaming
- **Requirements**: ~1GB RAM, internet for initial download

#### 2. Google Speech Recognition (Fallback)
- **Service**: Google's speech recognition API
- **Accuracy**: Good accuracy, requires internet
- **Processing**: Traditional listen-and-process approach
- **Requirements**: Internet connection

### Audio Processing
- **Sample Rate**: 16kHz
- **Channels**: Mono (1 channel)
- **Buffer Size**: 2-second chunks for processing
- **Noise Detection**: Energy-based silence detection

## Troubleshooting

### Common Issues

#### 1. "No speech detected"
- **Solution**: Check microphone permissions
- **Test**: Run `python test_speech.py`

#### 2. "Whisper not installed"
- **Solution**: Install with `pip install openai-whisper`
- **Alternative**: App will use fallback method

#### 3. "Audio device error"
- **Solution**: Check microphone connection
- **Test**: Verify in system sound settings

#### 4. "Speech recognition service error"
- **Solution**: Check internet connection
- **Alternative**: Use offline Whisper model

### Performance Tips

1. **Microphone Quality**: Use a good quality microphone for better accuracy
2. **Environment**: Reduce background noise
3. **Speaking**: Speak clearly and at normal volume
4. **Distance**: Keep microphone at consistent distance

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
- Whisper model installed

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
- Energy threshold in `process_audio_buffer` method
- Buffer size in audio callback

### Changing Whisper Model
Modify the model size in `init_models`:
- `"tiny"` - Fastest, least accurate
- `"base"` - Balanced (default)
- `"small"` - More accurate, slower
- `"medium"` - High accuracy, slower
- `"large"` - Best accuracy, slowest

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

- [ ] Offline voice command processing
- [ ] Multiple language support
- [ ] Custom wake word detection
- [ ] Voice activity detection improvements
- [ ] Integration with more system controls 