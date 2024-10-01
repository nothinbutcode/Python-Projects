import tkinter as tk
from tkinter import scrolledtext, ttk
import wave
import time
import threading
import numpy as np

# Function to install dependencies
def install_dependencies():
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "install_dependencies.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        user_input = input("Dependencies installation failed. Do you want to continue running the script anyway? (y/n): ")
        if user_input.lower() != 'y':
            sys.exit("Exiting due to failed dependencies installation.")

# Attempt to install dependencies
install_dependencies()

# Check if pyaudio can be imported, proceed with a warning if not
try:
    import pyaudio as pa
except ModuleNotFoundError:
    print("Warning: PyAudio is not installed or the _portaudio module is missing. Transcription may not work properly.")
    import portaudio

# Import remaining modules
import speech_recognition as sr
import whisper

# Initialize recognizer and Whisper model
recognizer = sr.Recognizer()
model = whisper.load_model("base")

# GUI class
class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Audio Transcription")
        
        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.language_label = tk.Label(root, text="Select Language:")
        self.language_label.pack(pady=10)

        self.language_var = tk.StringVar(value="auto")
        self.language_combobox = ttk.Combobox(root, textvariable=self.language_var, state="readonly")
        self.language_combobox['values'] = ["auto"] + sorted(whisper.tokenizer.LANGUAGES.keys())
        self.language_combobox.pack(pady=10)
        
        self.transcription_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.transcription_text.pack(pady=10)
        
        self.p = pa.PyAudio()  # Using 'pa' alias for PyAudio
        self.stream = None
        self.recording = False
        self.thread = None
        
        self.segment_duration = 30  # Duration in seconds
        self.pause_threshold = 10  # Pause threshold in seconds
        self.segment_frames = []
        self.segment_start_time = None
        self.last_speech_time = None

    def start_recording(self):
        self.recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.transcription_text.insert(tk.END, "Recording started...\n")
        self.thread = threading.Thread(target=self.live_audio_stream_to_segments)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.transcription_text.insert(tk.END, "Recording stopped.\n")

    def save_audio_segment(self, audio_data, filename):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(self.p.get_sample_size(pa.paInt16))  # Using 'pa' alias for paInt16
            wf.setframerate(44100)
            wf.writeframes(audio_data)

    def transcribe_audio_segment(self, filename):
        language = self.language_var.get()
        options = {} if language == "auto" else {"language": language}
        result = model.transcribe(filename, **options)
        return result['text']

    def listen_for_keyword(self, keyword):
        with sr.Microphone() as source:
            while not self.recording:
                self.transcription_text.insert(tk.END, f"Listening for '{keyword}'...\n")
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    if keyword in transcription.lower():
                        self.recording = True
                        self.transcription_text.insert(tk.END, "Keyword detected. Resuming recording...\n")
                        break
                except sr.UnknownValueError:
                    continue

    def live_audio_stream_to_segments(self):
        self.stream = self.p.open(format=pa.paInt16,  # Using 'pa' alias for paInt16
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)

        self.segment_frames = []
        self.segment_start_time = time.time()
        self.last_speech_time = time.time()

        while True:
            if self.recording:
                data = self.stream.read(1024)
                self.segment_frames.append(data)
                
                audio_data = np.frombuffer(data, dtype=np.int16)
                if np.abs(audio_data).mean() > 500:  # Adjust silence threshold as needed
                    self.last_speech_time = time.time()

                if time.time() - self.last_speech_time > self.pause_threshold:
                    self.transcription_text.insert(tk.END, "Detected 10 seconds of silence. Pausing recording...\n")
                    self.recording = False

                if time.time() - self.segment_start_time >= self.segment_duration:
                    segment_filename = f"segment_{int(time.time())}.wav"
                    self.save_audio_segment(b''.join(self.segment_frames), segment_filename)
                    self.transcription_text.insert(tk.END, f"Segment saved: {segment_filename}\n")

                    transcription = self.transcribe_audio_segment(segment_filename)
                    self.transcription_text.insert(tk.END, f"Transcription: {transcription}\n")

                    self.segment_frames = []
                    self.segment_start_time = time.time()

            else:
                self.listen_for_keyword("start translating")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def get_vb_cable_index(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if "VB-Audio Virtual Cable" in dev['name']:
                return i
        raise ValueError("VB-Audio Virtual Cable not found. Please ensure it is installed and configured correctly.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
