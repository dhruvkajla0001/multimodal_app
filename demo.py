#!/usr/bin/env python3
"""
Simple demo script to show the multimodal application concept.
This runs without requiring all dependencies to be installed.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

class DemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Multimodal AI Assistant - DEMO")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.running = False
        self.create_gui()
        
    def create_gui(self):
        """Create the demo GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🤖 Multimodal AI Assistant - DEMO MODE", 
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Demo info
        info_label = tk.Label(
            main_frame,
            text="This is a demo showing the interface and simulated functionality.\nInstall dependencies to use real AI models.",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#ecf0f1',
            justify=tk.CENTER
        )
        info_label.pack(pady=10)
        
        # Control button
        self.demo_button = tk.Button(
            main_frame,
            text="🎬 Start Demo",
            command=self.toggle_demo,
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            padx=30,
            pady=15
        )
        self.demo_button.pack(pady=20)
        
        # Model status frames
        models_frame = tk.Frame(main_frame, bg='#2c3e50')
        models_frame.pack(pady=20, fill=tk.X)
        
        # Gesture demo
        gesture_frame = tk.LabelFrame(
            models_frame,
            text="👋 Gesture Recognition (Demo)",
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
            text="Simulated gestures will appear here",
            bg='#34495e',
            fg='white',
            font=("Arial", 9)
        )
        self.gesture_info.pack(pady=5)
        
        # Speech demo
        speech_frame = tk.LabelFrame(
            models_frame,
            text="🎤 Speech Recognition (Demo)",
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
            text="Simulated voice commands will appear here",
            bg='#34495e',
            fg='white',
            font=("Arial", 9)
        )
        self.speech_info.pack(pady=5)
        
        # Object detection demo
        object_frame = tk.LabelFrame(
            models_frame,
            text="👁️ Object Detection (Demo)",
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
            text="Simulated object detections will appear here",
            bg='#34495e',
            fg='white',
            font=("Arial", 9)
        )
        self.object_info.pack(pady=5)
        
        # Camera feed demo
        camera_frame = tk.LabelFrame(
            main_frame,
            text="📹 Camera Feed (Demo)",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        camera_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.camera_label = tk.Label(
            camera_frame,
            text="📷 Camera feed would appear here\n(Requires OpenCV and camera)",
            bg='#34495e',
            fg='white',
            font=("Arial", 14),
            justify=tk.CENTER
        )
        self.camera_label.pack(expand=True)
        
        # Log frame
        log_frame = tk.LabelFrame(
            main_frame,
            text="📝 Activity Log (Demo)",
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
            height=6,
            bg='#2c3e50',
            fg='white',
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        scrollbar = tk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Instructions
        instructions = tk.Label(
            main_frame,
            text="💡 Instructions:\n1. Click 'Start Demo' to see simulated AI interactions\n2. Run 'python test_setup.py' to check dependencies\n3. Install dependencies with 'pip install -r requirements.txt'\n4. Run 'python main.py' for the full application",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#bdc3c7',
            justify=tk.LEFT
        )
        instructions.pack(pady=10)
        
        # Start update loop
        self.update_gui()
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        print(log_entry.strip())
        
    def toggle_demo(self):
        """Start or stop the demo"""
        if not self.running:
            self.start_demo()
        else:
            self.stop_demo()
            
    def start_demo(self):
        """Start the demo simulation"""
        self.running = True
        self.demo_button.config(text="⏹️ Stop Demo", bg='#e74c3c')
        
        # Start demo threads
        self.gesture_thread = threading.Thread(target=self.gesture_demo)
        self.gesture_thread.daemon = True
        self.gesture_thread.start()
        
        self.speech_thread = threading.Thread(target=self.speech_demo)
        self.speech_thread.daemon = True
        self.speech_thread.start()
        
        self.object_thread = threading.Thread(target=self.object_demo)
        self.object_thread.daemon = True
        self.object_thread.start()
        
        self.log_message("🎬 Demo started - simulating AI interactions...")
        
    def stop_demo(self):
        """Stop the demo simulation"""
        self.running = False
        self.demo_button.config(text="🎬 Start Demo", bg='#3498db')
        self.log_message("⏹️ Demo stopped")
        
    def gesture_demo(self):
        """Simulate gesture recognition"""
        gestures = [
            "VOLUME_UP", "VOLUME_DOWN", "BRIGHTNESS_UP", 
            "BRIGHTNESS_DOWN", "MOUSE_CONTROL", "SCREENSHOT"
        ]
        
        while self.running:
            time.sleep(3)
            if self.running:
                gesture = random.choice(gestures)
                self.log_message(f"👋 Gesture detected: {gesture}")
                
    def speech_demo(self):
        """Simulate speech recognition"""
        commands = [
            "volume up", "volume down", "brightness up", 
            "brightness down", "take screenshot", "open notepad"
        ]
        
        while self.running:
            time.sleep(4)
            if self.running:
                command = random.choice(commands)
                self.log_message(f"🎤 Speech: {command}")
                
    def object_demo(self):
        """Simulate object detection"""
        objects = [
            "person", "laptop", "mouse", "keyboard", "cup", 
            "bottle", "phone", "book", "chair", "table"
        ]
        
        while self.running:
            time.sleep(2.5)
            if self.running:
                obj = random.choice(objects)
                confidence = round(random.uniform(0.6, 0.95), 2)
                self.log_message(f"👁️ Detected: {obj} ({confidence})")
                
    def update_gui(self):
        """Update GUI elements"""
        try:
            # Update status indicators
            if self.running:
                self.gesture_status.config(text="Status: Running", fg='#27ae60')
                self.speech_status.config(text="Status: Running", fg='#27ae60')
                self.object_status.config(text="Status: Running", fg='#27ae60')
            else:
                self.gesture_status.config(text="Status: Stopped", fg='#e74c3c')
                self.speech_status.config(text="Status: Stopped", fg='#e74c3c')
                self.object_status.config(text="Status: Stopped", fg='#e74c3c')
                
        except Exception as e:
            print(f"GUI update error: {str(e)}")
        
        # Schedule next update
        self.root.after(100, self.update_gui)

def main():
    root = tk.Tk()
    app = DemoApp(root)
    
    def on_closing():
        app.stop_demo()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 