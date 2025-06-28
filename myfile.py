# EVA: Advanced Multimodal AI Assistant (Polished Edition)
# With Gesture Control, Object Detection, Voice Commands, TTS (Female), and Real-time GUI

import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import time
import queue
import cv2
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import pyttsx3
import pyautogui
import screen_brightness_control as sbc
import speech_recognition as sr
import mediapipe as mp
from PIL import Image, ImageTk
from ultralytics import YOLO
import whisper

class EVA:
    def __init__(self, root):
        self.root = root
        self.root.title("EVA - Multimodal AI Assistant")
        self.root.geometry("1280x800")
        self.root.configure(bg="#1e272e")

        # Initialize AI modules
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_loop, daemon=True).start()

        self.sample_rate = 16000
        self.audio_buffer = []
        self.whisper_model = whisper.load_model("base")
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.speech_running = False
        self.cap = cv2.VideoCapture(0)

        # Queues for async updates
        self.transcription_queue = asyncio.Queue()
        self.object_queue = asyncio.Queue()
        self.gesture_queue = asyncio.Queue()

        # Text-to-Speech (female voice)
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 170)
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break

        # Models
        self.yolo = YOLO("yolov8n.pt")
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.drawing = mp.solutions.drawing_utils

        # UI Setup
        self.setup_ui()

        # Start tasks
        self.running = True
        self.loop.call_soon_threadsafe(lambda: self.loop.create_task(self.run_all()))

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def setup_ui(self):
        title = tk.Label(self.root, text="🤖 EVA: Multimodal Assistant", font=("Arial", 24, "bold"), bg="#1e272e", fg="white")
        title.pack(pady=10)

        self.status_text = tk.Label(self.root, text="Initializing...", font=("Arial", 14), bg="#1e272e", fg="#00d2d3")
        self.status_text.pack(pady=5)

        self.transcription_label = tk.Label(self.root, text="Waiting for speech...", font=("Arial", 14), bg="#1e272e", fg="#feca57")
        self.transcription_label.pack(pady=5)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    def say(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def log(self, msg):
        print(f"[EVA] {msg}")
        self.status_text.config(text=msg)

    async def run_all(self):
        await asyncio.gather(
            self.speech_loop(),
            self.camera_loop(),
            self.gui_update_loop()
        )

    async def speech_loop(self):
        self.log("🎤 Voice system online")
        self.speech_running = True

        def audio_callback(indata, frames, time, status):
            if self.speech_running:
                audio_data = indata[:, 0].astype(np.float32)
                self.audio_buffer.extend(audio_data)
                if len(self.audio_buffer) >= self.sample_rate * 2:
                    asyncio.run_coroutine_threadsafe(self.process_audio(), self.loop)

        with sd.InputStream(callback=audio_callback, channels=1, samplerate=self.sample_rate, dtype=np.float32):
            while self.speech_running:
                await asyncio.sleep(0.1)

    async def process_audio(self):
        audio_data = np.array(self.audio_buffer[:self.sample_rate * 2])
        self.audio_buffer = self.audio_buffer[self.sample_rate * 2:]

        if np.mean(audio_data ** 2) < 0.001:
            return

        # Convert float32 audio to int16
        audio_int16 = np.int16(audio_data * 32767)

        # ✅ Save audio to a real file after the file is closed
        temp_filename = os.path.join(tempfile.gettempdir(), f"eva_temp_{int(time.time())}.wav")
        try:
            wav.write(temp_filename, self.sample_rate, audio_int16)

            if not os.path.exists(temp_filename):
                self.log(f"❌ Temp file not found: {temp_filename}")
                return

            result = self.whisper_model.transcribe(temp_filename, language="en")
            transcription = result['text'].strip()
            if transcription:
                await self.transcription_queue.put(transcription)
                await self.handle_command(transcription.lower())
        except Exception as e:
            self.log(f"⚠️ Whisper error: {e}")
        finally:
            try:
                os.remove(temp_filename)
            except Exception as e:
                self.log(f"⚠️ Failed to delete temp file: {e}")


    async def handle_command(self, text):
        self.say(text)
        if "volume up" in text:
            pyautogui.press("volumeup")
        elif "volume down" in text:
            pyautogui.press("volumedown")
        elif "mute" in text:
            pyautogui.press("volumemute")
        elif "brightness up" in text:
            sbc.set_brightness(min(100, sbc.get_brightness()[0] + 10))
        elif "brightness down" in text:
            sbc.set_brightness(max(0, sbc.get_brightness()[0] - 10))
        elif "screenshot" in text:
            img = pyautogui.screenshot()
            img.save(f"screenshot_{int(time.time())}.png")
            self.say("Screenshot taken")

    async def camera_loop(self):
        self.log("📷 Camera feed started")
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    self.drawing.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
                    gesture = self.interpret_gesture(hand)
                    if gesture:
                        await self.gesture_queue.put(gesture)
                        await self.handle_command(gesture)

            yolo_results = self.yolo(frame, verbose=False)
            for det in yolo_results:
                for box in det.boxes:
                    cls_id = int(box.cls[0])
                    name = self.yolo.names[cls_id]
                    conf = float(box.conf[0])
                    if conf > 0.5:
                        await self.object_queue.put(name)
                        await self.handle_command(name)

            frame = cv2.resize(frame, (640, 480))
            img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.image_label.config(image=img)
            self.image_label.image = img

            await asyncio.sleep(0.03)

    def interpret_gesture(self, hand):
        points = [ [lm.x, lm.y] for lm in hand.landmark ]
        if points[4][1] < points[3][1] and points[8][1] > points[6][1]:
            return "volume up"
        if points[4][1] > points[3][1] and points[8][1] > points[6][1]:
            return "volume down"
        if points[8][1] < points[6][1] and points[12][1] < points[10][1]:
            return "screenshot"
        return None

    async def gui_update_loop(self):
        while self.running:
            try:
                text = await asyncio.wait_for(self.transcription_queue.get(), timeout=0.1)
                self.transcription_label.config(text=text)
            except asyncio.TimeoutError:
                pass
            await asyncio.sleep(0.1)

def main():
    root = tk.Tk()
    app = EVA(root)
    def on_close():
        app.running = False
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
