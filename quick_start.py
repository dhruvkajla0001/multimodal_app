#!/usr/bin/env python3
"""
Quick start script for the Multimodal AI Assistant.
This script helps users get started with the application.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

class QuickStart:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Multimodal AI Assistant - Quick Start")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        self.create_gui()
        
    def create_gui(self):
        """Create the quick start GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🚀 Multimodal AI Assistant",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            main_frame,
            text="Quick Start Guide",
            font=("Arial", 16),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        subtitle_label.pack(pady=5)
        
        # Progress frame
        progress_frame = tk.LabelFrame(
            main_frame,
            text="📋 Setup Progress",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        progress_frame.pack(pady=20, fill=tk.X)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(pady=10, padx=10, fill=tk.X)
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to start setup...",
            bg='#34495e',
            fg='white',
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(pady=20)
        
        # Setup button
        self.setup_button = tk.Button(
            buttons_frame,
            text="🔧 Run Setup",
            command=self.run_setup,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10
        )
        self.setup_button.pack(side=tk.LEFT, padx=10)
        
        # Test button
        self.test_button = tk.Button(
            buttons_frame,
            text="🧪 Test Setup",
            command=self.test_setup,
            font=("Arial", 12, "bold"),
            bg='#f39c12',
            fg='white',
            padx=20,
            pady=10
        )
        self.test_button.pack(side=tk.LEFT, padx=10)
        
        # Demo button
        self.demo_button = tk.Button(
            buttons_frame,
            text="🎬 Run Demo",
            command=self.run_demo,
            font=("Arial", 12, "bold"),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=10
        )
        self.demo_button.pack(side=tk.LEFT, padx=10)
        
        # Launch button
        self.launch_button = tk.Button(
            buttons_frame,
            text="🚀 Launch App",
            command=self.launch_app,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10
        )
        self.launch_button.pack(side=tk.LEFT, padx=10)
        
        # Instructions
        instructions_frame = tk.LabelFrame(
            main_frame,
            text="📖 Instructions",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        instructions_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        instructions_text = """
1. 🔧 Run Setup: Install all required dependencies
2. 🧪 Test Setup: Verify everything is working correctly
3. 🎬 Run Demo: See the interface without real AI models
4. 🚀 Launch App: Start the full multimodal application

Requirements:
• Python 3.8 or higher
• Webcam
• Microphone
• Internet connection (for model downloads)
• Windows 10/11 (for system controls)

Note: The setup process may take several minutes to download AI models.
        """
        
        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            bg='#34495e',
            fg='white',
            font=("Arial", 10),
            justify=tk.LEFT
        )
        instructions_label.pack(pady=10, padx=10)
        
    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update()
        
    def run_setup(self):
        """Run the setup process"""
        try:
            self.setup_button.config(state=tk.DISABLED)
            self.update_progress(10, "Installing dependencies...")
            
            # Install requirements
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.update_progress(50, "Dependencies installed successfully!")
                self.update_progress(75, "Downloading AI models...")
                
                # Download YOLO model
                try:
                    subprocess.run([
                        sys.executable, "-c", 
                        "from ultralytics import YOLO; YOLO('yolov8n.pt')"
                    ], capture_output=True)
                    self.update_progress(100, "Setup completed successfully!")
                    messagebox.showinfo("Success", "Setup completed! You can now test or launch the application.")
                except Exception as e:
                    self.update_progress(100, f"Setup completed with warnings: {str(e)}")
                    messagebox.showwarning("Warning", f"Setup completed but with warnings: {str(e)}")
            else:
                self.update_progress(100, f"Setup failed: {result.stderr}")
                messagebox.showerror("Error", f"Setup failed:\n{result.stderr}")
                
        except Exception as e:
            self.update_progress(100, f"Setup error: {str(e)}")
            messagebox.showerror("Error", f"Setup error: {str(e)}")
        finally:
            self.setup_button.config(state=tk.NORMAL)
            
    def test_setup(self):
        """Test the setup"""
        try:
            self.test_button.config(state=tk.DISABLED)
            self.update_progress(0, "Running tests...")
            
            result = subprocess.run([
                sys.executable, "test_setup.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.update_progress(100, "All tests passed!")
                messagebox.showinfo("Success", "All tests passed! Your setup is ready.")
            else:
                self.update_progress(100, "Some tests failed")
                messagebox.showwarning("Warning", f"Some tests failed:\n{result.stdout}")
                
        except Exception as e:
            self.update_progress(100, f"Test error: {str(e)}")
            messagebox.showerror("Error", f"Test error: {str(e)}")
        finally:
            self.test_button.config(state=tk.NORMAL)
            
    def run_demo(self):
        """Run the demo"""
        try:
            self.demo_button.config(state=tk.DISABLED)
            self.update_progress(0, "Starting demo...")
            
            # Close this window and start demo
            self.root.destroy()
            subprocess.Popen([sys.executable, "demo.py"])
            
        except Exception as e:
            self.update_progress(100, f"Demo error: {str(e)}")
            messagebox.showerror("Error", f"Demo error: {str(e)}")
            self.demo_button.config(state=tk.NORMAL)
            
    def launch_app(self):
        """Launch the main application"""
        try:
            self.launch_button.config(state=tk.DISABLED)
            self.update_progress(0, "Starting application...")
            
            # Close this window and start main app
            self.root.destroy()
            subprocess.Popen([sys.executable, "main.py"])
            
        except Exception as e:
            self.update_progress(100, f"Launch error: {str(e)}")
            messagebox.showerror("Error", f"Launch error: {str(e)}")
            self.launch_button.config(state=tk.NORMAL)

def main():
    app = QuickStart()
    app.root.mainloop()

if __name__ == "__main__":
    main() 