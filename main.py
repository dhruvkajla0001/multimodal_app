import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import queue
import time
import cv2
import numpy as np
from PIL import Image, ImageTk
import speech_recognition as sr
import mediapipe as mp
from ultralytics import YOLO
import pyautogui
import screen_brightness_control as sbc
import psutil
import os
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import wave
from concurrent.futures import ThreadPoolExecutor
import threading

class MultimodalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multimodal AI Assistant (Async)")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize asyncio components
        self.loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Initialize queues for inter-thread communication
        self.gesture_queue = asyncio.Queue()
        self.speech_queue = asyncio.Queue()
        self.object_queue = asyncio.Queue()
        self.transcription_queue = asyncio.Queue()
        
        # Control flags
        self.running = False
        self.gesture_running = False
        self.speech_running = False
        self.object_running = False
        
        # Speech-to-text variables
        self.current_transcription = ""
        self.audio_buffer = []
        self.sample_rate = 16000
        
        # Async tasks
        self.gesture_task = None
        self.speech_task = None
        self.object_task = None
        self.gui_update_task = None
        
        # Create GUI first
        self.create_gui()
        
        # Initialize models
        self.init_models()
        
        # Initialize camera
        self.cap = None
        
    def init_models(self):
        """Initialize all AI models"""
        try:
            # MediaPipe for gesture recognition
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.mp_drawing = mp.solutions.drawing_utils
            
            # YOLO for object detection
            self.yolo_model = YOLO('yolov8n.pt')
            
            # Speech recognition (legacy)
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            print("All models initialized successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize models: {str(e)}")
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🤖 Multimodal AI Assistant", 
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(pady=10)
        
        # Start/Stop button
        self.start_button = tk.Button(
            control_frame,
            text="🚀 Start All Models",
            command=self.toggle_models,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Individual model controls
        model_controls = tk.Frame(main_frame, bg='#2c3e50')
        model_controls.pack(pady=10)
        
        # Gesture control
        gesture_frame = tk.LabelFrame(
            model_controls,
            text="👋 Gesture Recognition",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        gesture_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.gesture_status = tk.Label(
            gesture_frame,
            text="Status: Stopped",
            bg='#34495e',
            fg='#e74c3c',
            font=("Arial", 10)
        )
        self.gesture_status.pack(pady=5)
        
        self.gesture_info = tk.Label(
            gesture_frame,
            text="No gesture detected",
            bg='#34495e',
            fg='white',
            font=("Arial", 9)
        )
        self.gesture_info.pack(pady=5)
        
        # Speech control
        speech_frame = tk.LabelFrame(
            model_controls,
            text="🎤 Speech Recognition",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        speech_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.speech_status = tk.Label(
            speech_frame,
            text="Status: Stopped",
            bg='#34495e',
            fg='#e74c3c',
            font=("Arial", 10)
        )
        self.speech_status.pack(pady=5)
        
        self.speech_info = tk.Label(
            speech_frame,
            text="No speech detected",
            bg='#34495e',
            fg='white',
            font=("Arial", 9)
        )
        self.speech_info.pack(pady=5)
        
        # Object detection
        object_frame = tk.LabelFrame(
            model_controls,
            text="👁️ Object Detection",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        object_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.object_status = tk.Label(
            object_frame,
            text="Status: Stopped",
            bg='#34495e',
            fg='#e74c3c',
            font=("Arial", 10)
        )
        self.object_status.pack(pady=5)
        
        self.object_info = tk.Label(
            object_frame,
            text="No objects detected",
            bg='#34495e',
            fg='white',
            font=("Arial", 9)
        )
        self.object_info.pack(pady=5)
        
        # Camera feed frame
        camera_frame = tk.LabelFrame(
            main_frame,
            text="📹 Camera Feed",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        camera_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.camera_label = tk.Label(
            camera_frame,
            text="Camera not started",
            bg='#34495e',
            fg='white',
            font=("Arial", 14)
        )
        self.camera_label.pack(expand=True)
        
        # Speech-to-Text Transcription Display
        transcription_frame = tk.LabelFrame(
            main_frame,
            text="🎤 Live Speech Transcription",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        transcription_frame.pack(pady=5, fill=tk.X)
        
        self.transcription_label = tk.Label(
            transcription_frame,
            text="Waiting for speech...",
            bg='#2c3e50',
            fg='#27ae60',
            font=("Arial", 14, "bold"),
            wraplength=1100,
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        self.transcription_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Log frame
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 Activity Log",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        log_container = tk.Frame(log_frame, bg='#34495e')
        log_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(
            log_container,
            height=8,
            bg='#2c3e50',
            fg='white',
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        scrollbar = tk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Note: GUI updates are now handled by async_gui_update method
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        print(log_entry.strip())
    
    def toggle_models(self):
        """Start or stop all models"""
        if not self.running:
            self.start_all_models()
        else:
            self.stop_all_models()
    
    def start_all_models(self):
        """Start all three models in separate async tasks"""
        try:
            self.running = True
            self.start_button.config(text="⏹️ Stop All Models", bg='#e74c3c')
            
            # Start camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Cannot open camera")
            
            # Start asyncio loop in a separate thread
            def run_async_loop():
                asyncio.set_event_loop(self.loop)
                self.loop.run_forever()
            
            self.async_thread = threading.Thread(target=run_async_loop, daemon=True)
            self.async_thread.start()
            
            # Start all async tasks
            self.gesture_running = True
            self.speech_running = True
            self.object_running = True
            
            # Schedule tasks to start
            self.loop.call_soon_threadsafe(self._start_async_tasks)
            
            self.log_message("🚀 All models started successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Error starting models: {str(e)}")
            self.stop_all_models()
    
    def _start_async_tasks(self):
        """Start all async tasks"""
        self.gesture_task = self.loop.create_task(self.gesture_recognition_loop())
        self.speech_task = self.loop.create_task(self.speech_recognition_loop())
        self.object_task = self.loop.create_task(self.object_detection_loop())
        self.gui_update_task = self.loop.create_task(self.async_gui_update())
    
    def stop_all_models(self):
        """Stop all models"""
        self.running = False
        self.gesture_running = False
        self.speech_running = False
        self.object_running = False
        
        # Cancel async tasks
        if self.gesture_task:
            self.gesture_task.cancel()
        if self.speech_task:
            self.speech_task.cancel()
        if self.object_task:
            self.object_task.cancel()
        if self.gui_update_task:
            self.gui_update_task.cancel()
        
        # Stop asyncio loop
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.start_button.config(text="🚀 Start All Models", bg='#27ae60')
        self.log_message("⏹️ All models stopped")
    
    async def gesture_recognition_loop(self):
        """Main loop for gesture recognition"""
        self.log_message("👋 Gesture recognition started")
        
        while self.gesture_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw landmarks
                        self.mp_drawing.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                        )
                        
                        # Analyze gesture
                        gesture = self.analyze_gesture(hand_landmarks)
                        if gesture:
                            await self.gesture_queue.put(gesture)
                            self.log_message(f"👋 Gesture detected: {gesture}")
                
                # Convert frame for Tkinter display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_pil = frame_pil.resize((640, 480))
                frame_tk = ImageTk.PhotoImage(frame_pil)
                
                # Update camera display
                self.camera_label.config(image=frame_tk, text="")
                self.camera_label.image = frame_tk
                
                await asyncio.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                self.log_message(f"❌ Gesture recognition error: {str(e)}")
                break
        
        self.log_message("👋 Gesture recognition stopped")
    
    def analyze_gesture(self, landmarks):
        """Analyze hand landmarks to determine gesture"""
        try:
            # Get landmark coordinates
            points = []
            for lm in landmarks.landmark:
                points.append([lm.x, lm.y, lm.z])
            
            # Calculate distances and angles
            thumb_tip = points[4]
            index_tip = points[8]
            middle_tip = points[12]
            ring_tip = points[16]
            pinky_tip = points[20]
            
            # Volume control gesture (thumb up/down)
            if self.is_volume_gesture(points):
                if thumb_tip[1] < points[3][1]:  # Thumb pointing up
                    return "VOLUME_UP"
                else:  # Thumb pointing down
                    return "VOLUME_DOWN"
            
            # Brightness control gesture (index finger up/down)
            if self.is_brightness_gesture(points):
                if index_tip[1] < points[6][1]:  # Index pointing up
                    return "BRIGHTNESS_UP"
                else:  # Index pointing down
                    return "BRIGHTNESS_DOWN"
            
            # Mouse control gesture (open palm)
            if self.is_mouse_gesture(points):
                return "MOUSE_CONTROL"
            
            # Screenshot gesture (peace sign)
            if self.is_screenshot_gesture(points):
                return "SCREENSHOT"
            
            return None
            
        except Exception as e:
            return None
    
    def is_volume_gesture(self, points):
        """Check if gesture is for volume control"""
        # Thumb extended, other fingers closed
        thumb_tip = points[4]
        thumb_ip = points[3]
        index_tip = points[8]
        middle_tip = points[12]
        
        # Check if thumb is extended and others are closed
        return (abs(thumb_tip[0] - thumb_ip[0]) > 0.05 and 
                index_tip[1] > points[6][1] and 
                middle_tip[1] > points[10][1])
    
    def is_brightness_gesture(self, points):
        """Check if gesture is for brightness control"""
        # Index finger extended, others closed
        index_tip = points[8]
        middle_tip = points[12]
        ring_tip = points[16]
        
        return (index_tip[1] < points[6][1] and 
                middle_tip[1] > points[10][1] and 
                ring_tip[1] > points[14][1])
    
    def is_mouse_gesture(self, points):
        """Check if gesture is for mouse control"""
        # All fingers extended (open palm)
        return all(points[i][1] < points[i-2][1] for i in [8, 12, 16, 20])
    
    def is_screenshot_gesture(self, points):
        """Check if gesture is for screenshot (peace sign)"""
        # Index and middle fingers extended, others closed
        index_tip = points[8]
        middle_tip = points[12]
        ring_tip = points[16]
        pinky_tip = points[20]
        
        return (index_tip[1] < points[6][1] and 
                middle_tip[1] < points[10][1] and 
                ring_tip[1] > points[14][1] and 
                pinky_tip[1] > points[18][1])
    
    async def speech_recognition_loop(self):
        """Main loop for speech recognition with real-time transcription"""
        self.log_message("🎤 Speech recognition started")
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.log_message("🎤 Ambient noise adjusted")
            
            while self.speech_running:
                try:
                    # Run blocking speech recognition in thread pool
                    loop = asyncio.get_event_loop()
                    
                    # Listen for audio
                    audio = await loop.run_in_executor(
                        self.executor,
                        self._listen_for_audio
                    )
                    
                    if audio:
                        # Recognize speech
                        text = await loop.run_in_executor(
                            self.executor,
                            self._recognize_audio,
                            audio
                        )
                        
                        if text:
                            # Update transcription display
                            self.current_transcription = text
                            await self.transcription_queue.put(text)
                            await self.speech_queue.put(text.lower())
                            self.log_message(f"🎤 Transcribed: {text}")
                            
                            # Process voice commands
                            await self.process_voice_command(text.lower())
                            
                except Exception as e:
                    if self.speech_running:  # Only log if not intentionally stopped
                        self.log_message(f"❌ Speech recognition error: {str(e)}")
                    break
                    
        except Exception as e:
            self.log_message(f"❌ Speech recognition error: {str(e)}")
        
        self.log_message("🎤 Speech recognition stopped")
    
    def _listen_for_audio(self):
        """Blocking method to listen for audio"""
        try:
            with self.microphone as source:
                return self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
        except:
            return None
    
    def _recognize_audio(self, audio):
        """Blocking method to recognize audio"""
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            self.log_message(f"❌ Speech recognition service error: {str(e)}")
            return None
    
    async def recognize_speech(self, audio_file):
        """Recognize speech from audio file using speech_recognition"""
        try:
            loop = asyncio.get_event_loop()
            
            # Load audio file
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Recognize speech
            text = await loop.run_in_executor(
                self.executor,
                self._recognize_audio,
                audio
            )
            
            return text
            
        except Exception as e:
            self.log_message(f"❌ Speech recognition error: {str(e)}")
            return None
    
    async def process_voice_command(self, command):
        """Process voice commands"""
        try:
            if "volume up" in command or "increase volume" in command:
                pyautogui.press('volumeup')
                self.log_message("🔊 Volume increased")
                
            elif "volume down" in command or "decrease volume" in command:
                pyautogui.press('volumedown')
                self.log_message("🔊 Volume decreased")
                
            elif "mute" in command or "unmute" in command:
                pyautogui.press('volumemute')
                self.log_message("🔇 Volume toggled")
                
            elif "brightness up" in command or "increase brightness" in command:
                current = sbc.get_brightness()[0]
                sbc.set_brightness(min(100, current + 10))
                self.log_message("💡 Brightness increased")
                
            elif "brightness down" in command or "decrease brightness" in command:
                current = sbc.get_brightness()[0]
                sbc.set_brightness(max(0, current - 10))
                self.log_message("💡 Brightness decreased")
                
            elif "screenshot" in command or "take screenshot" in command:
                screenshot = pyautogui.screenshot()
                screenshot.save(f"screenshot_{int(time.time())}.png")
                self.log_message("📸 Screenshot taken")
                
            elif "open notepad" in command:
                os.system("notepad")
                self.log_message("📝 Notepad opened")
                
            elif "open calculator" in command:
                os.system("calc")
                self.log_message("🧮 Calculator opened")
                
            elif "close" in command or "exit" in command:
                self.log_message("👋 Goodbye!")
                self.root.after(1000, self.root.quit)
                
        except Exception as e:
            self.log_message(f"❌ Voice command error: {str(e)}")
    
    async def object_detection_loop(self):
        """Main loop for object detection"""
        self.log_message("👁️ Object detection started")
        
        while self.object_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Run YOLO detection
                results = self.yolo_model(frame, verbose=False)
                
                detected_objects = []
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            # Get box coordinates
                            x1, y1, x2, y2 = box.xyxy[0]
                            confidence = box.conf[0]
                            class_id = int(box.cls[0])
                            class_name = self.yolo_model.names[class_id]
                            
                            if confidence > 0.5:  # Confidence threshold
                                detected_objects.append({
                                    'name': class_name,
                                    'confidence': float(confidence),
                                    'bbox': [int(x1), int(y1), int(x2), int(y2)]
                                })
                
                if detected_objects:
                    # Get most confident detection
                    best_detection = max(detected_objects, key=lambda x: x['confidence'])
                    await self.object_queue.put(best_detection)
                    self.log_message(f"👁️ Detected: {best_detection['name']} ({best_detection['confidence']:.2f})")
                
                await asyncio.sleep(0.1)  # Reduce CPU usage
                
            except Exception as e:
                self.log_message(f"❌ Object detection error: {str(e)}")
                break
        
        self.log_message("👁️ Object detection stopped")
    
    async def async_gui_update(self):
        """Async GUI update loop"""
        while self.running:
            try:
                # Update gesture info
                try:
                    gesture = await asyncio.wait_for(self.gesture_queue.get(), timeout=0.1)
                    self.gesture_info.config(text=f"Last: {gesture}")
                except asyncio.TimeoutError:
                    pass
                
                # Update speech info
                try:
                    speech = await asyncio.wait_for(self.speech_queue.get(), timeout=0.1)
                    self.speech_info.config(text=f"Last: {speech[:30]}...")
                except asyncio.TimeoutError:
                    pass
                
                # Update transcription display
                try:
                    transcription = await asyncio.wait_for(self.transcription_queue.get(), timeout=0.1)
                    self.transcription_label.config(text=transcription, fg='#27ae60')
                    # Keep transcription visible for 5 seconds
                    self.root.after(5000, lambda: self.transcription_label.config(text="Waiting for speech...", fg='#27ae60'))
                except asyncio.TimeoutError:
                    pass
                
                # Update object info
                try:
                    obj = await asyncio.wait_for(self.object_queue.get(), timeout=0.1)
                    self.object_info.config(text=f"Last: {obj['name']}")
                except asyncio.TimeoutError:
                    pass
                
                # Update status indicators
                if self.gesture_running:
                    self.gesture_status.config(text="Status: Running", fg='#27ae60')
                else:
                    self.gesture_status.config(text="Status: Stopped", fg='#e74c3c')
                
                if self.speech_running:
                    self.speech_status.config(text="Status: Running", fg='#27ae60')
                else:
                    self.speech_status.config(text="Status: Stopped", fg='#e74c3c')
                
                if self.object_running:
                    self.object_status.config(text="Status: Running", fg='#27ae60')
                else:
                    self.object_status.config(text="Status: Stopped", fg='#e74c3c')
                
            except Exception as e:
                print(f"Async GUI update error: {str(e)}")
            
            await asyncio.sleep(0.1)  # Update every 100ms

def main():
    root = tk.Tk()
    app = MultimodalApp(root)
    
    # Handle window close
    def on_closing():
        app.stop_all_models()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 