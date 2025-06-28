#!/usr/bin/env python3
"""
Test script for speech recognition functionality
"""

import speech_recognition as sr
import sounddevice as sd
import numpy as np
import time

def test_basic_speech_recognition():
    """Test basic speech recognition"""
    print("🎤 Testing basic speech recognition...")
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        with microphone as source:
            print("Adjusting for ambient noise... Please be quiet.")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Ambient noise adjustment complete.")
        
        print("🎤 Please speak something (5 seconds)...")
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Transcribed: '{text}'")
        return True
        
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_audio_devices():
    """Test audio device availability"""
    print("🔊 Testing audio devices...")
    
    try:
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices:")
        
        for i, device in enumerate(devices):
            name = device.get('name', 'Unknown')
            max_inputs = device.get('max_inputs', 0)
            max_outputs = device.get('max_outputs', 0)
            print(f"  {i}: {name} (inputs: {max_inputs}, outputs: {max_outputs})")
        
        try:
            default_input = sd.query_devices(kind='input')
            print(f"Default input device: {default_input.get('name', 'Unknown')}")
        except Exception as e:
            print(f"Could not get default input device: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error querying audio devices: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Speech Recognition Test Suite")
    print("=" * 40)
    
    tests = [
        ("Audio Devices", test_audio_devices),
        ("Basic Speech Recognition", test_basic_speech_recognition),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Speech recognition should work properly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 