#!/usr/bin/env python3
"""
Test script to verify all dependencies and models are working correctly.
Run this before starting the main application.
"""

import sys
import importlib
import subprocess

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - FAILED: {e}")
        return False

def test_camera():
    """Test camera access"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera - OK")
                return True
            else:
                print("❌ Camera - FAILED: Cannot read frame")
                return False
        else:
            print("❌ Camera - FAILED: Cannot open camera")
            return False
    except Exception as e:
        print(f"❌ Camera - FAILED: {e}")
        return False

def test_microphone():
    """Test microphone access"""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic = sr.Microphone()
        print("✅ Microphone - OK")
        return True
    except Exception as e:
        print(f"❌ Microphone - FAILED: {e}")
        return False

def test_yolo():
    """Test YOLO model"""
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')
        print("✅ YOLO Model - OK")
        return True
    except Exception as e:
        print(f"❌ YOLO Model - FAILED: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe"""
    try:
        import mediapipe as mp
        hands = mp.solutions.hands.Hands()
        print("✅ MediaPipe - OK")
        return True
    except Exception as e:
        print(f"❌ MediaPipe - FAILED: {e}")
        return False

def test_system_controls():
    """Test system control functions"""
    try:
        import pyautogui
        import screen_brightness_control as sbc
        print("✅ System Controls - OK")
        return True
    except Exception as e:
        print(f"❌ System Controls - FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Testing Multimodal AI Assistant Setup...")
    print("=" * 50)
    
    tests = [
        ("OpenCV", lambda: test_import("cv2", "OpenCV")),
        ("NumPy", lambda: test_import("numpy", "NumPy")),
        ("PIL/Pillow", lambda: test_import("PIL", "Pillow")),
        ("Tkinter", lambda: test_import("tkinter", "Tkinter")),
        ("Speech Recognition", lambda: test_import("speech_recognition", "SpeechRecognition")),
        ("MediaPipe", test_mediapipe),
        ("YOLO", test_yolo),
        ("PyAutoGUI", lambda: test_import("pyautogui", "PyAutoGUI")),
        ("Screen Brightness Control", lambda: test_import("screen_brightness_control", "Screen Brightness Control")),
        ("Camera", test_camera),
        ("Microphone", test_microphone),
        ("System Controls", test_system_controls),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! You're ready to run the main application.")
        print("\nTo start the application, run:")
        print("python main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")
        
        if not test_import("ultralytics"):
            print("\nTo install YOLO, run:")
            print("pip install ultralytics")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 