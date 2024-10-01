import numpy as np
import sounddevice as sd
from pynput import keyboard
from faster_whisper import WhisperModel
import tempfile
from scipy.io.wavfile import write
import os
from deep_translator import GoogleTranslator

class FasterWhisperTranscriber:
    def __init__(self, model_size="large-v3", samplerate=44100, stero_or_audio=1):
        # Initialize the model size, sample rate, self.stero_or_audio, and Whisper model
        self.model_size = model_size
        self.sample_rate = samplerate
        self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
        self.is_recording = False
        self.detected_language = None  # Will be set during transcription
        self.target_language = 'en'  # Default target language
        self.stero_or_audio = stero_or_audio
        
    def on_press(self, key):
        # Start recording when the spacebar is pressed
        if key == keyboard.Key.space:
            if not self.is_recording:
                self.is_recording = True
                print("Recording started...")
    
    def on_release(self, key):
        # Stop recording when the spacebar is released
        if key == keyboard.Key.space:
            if self.is_recording:
                self.is_recording = False
                print("Stopped recording.")
                return False  # Stop listener
    
    def record_audio(self):
        # Initialize an empty array to store the recording
        recording = np.array([], dtype="float64").reshape(0, self.stero_or_audio)
        frames_per_buffer = int(self.sample_rate * 0.1)  # Set the number of frames per buffer
        
        # Listen for keyboard events to start and stop recording
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while True:
                if self.is_recording:
                    # Record a chunk of audio
                    chunk = self.input_stream.read(frames_per_buffer)
                    # Append the recorded chunk to the array
                    recording = np.vstack([recording, chunk])
                if not self.is_recording and len(recording) > 0:
                    break  # Stop recording when spacebar is released
            listener.join()
            
        return recording
    
    def save_temp_audio(self, recording):
        try:
            # Save the recorded audio to a temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_filename = temp_file.name
                write(temp_filename, self.sample_rate, recording)
                print(f"Temporary WAV file saved: {temp_filename}")
                return temp_filename
        except Exception as e:
            # Handle any errors that occur during saving
            print(f"Error saving temporary audio file: {e}")
            return None
    
    def transcribe_audio(self, file_path):
        try:
            # Transcribe the audio file using Whisper model
            segments, info = self.model.transcribe(file_path, beam_size=5)
            self.detected_language = info.language  # Set detected language
            print(f"Detected language: {self.detected_language}")
            full_transcription = ""
            for segment in segments:
                # Print and concatenate each segment of the transcription
                print(segment.text)
                full_transcription += segment.text + " "
            return full_transcription.strip()
        except Exception as e:
            # Handle any errors that occur during transcription
            print(f"Error transcribing audio: {e}")
            return None
        finally:
            # Remove the temporary audio file after transcription
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"Temporary file removed: {file_path}")
    
    def translate_text(self, text, target_lang='en'):
        try:
            # Translate the transcribed text using GoogleTranslator
            translator = GoogleTranslator(source=self.detected_language, target=target_lang)
            translated_text = translator.translate(text=text)
            return translated_text
        except Exception as e:
            # Handle any errors that occur during translation
            print(f"Translation error: {e}")
            return None
    
    def run(self):
        print("Hold spacebar to record")
        while True:
            try:
                # Record audio when spacebar is pressed
                recording = self.record_audio()
                if recording is None:
                    continue
                
                # Save the recorded audio to a temporary file
                file_path = self.save_temp_audio(recording)
                if file_path:
                    # Transcribe the audio file
                    transcription = self.transcribe_audio(file_path)
                    if transcription:
                        print(f"Transcription: {transcription}")
                        # Translate the transcribed text to the target language
                        translated_text = self.translate_text(transcription, target_lang='en')  # Assuming 'en' (eNGLISH) as the target language
                        if translated_text:
                            print(f"Translated text to en: {translated_text}")
                        
            except KeyboardInterrupt:
                # Exit the program when Ctrl+C is pressed
                print("\nExiting...")
                break
            except Exception as e:
                # Handle any other errors that occur
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    # Create an instance of FasterWhisperTranscriber and run the application
    transcriber = FasterWhisperTranscriber()
    transcriber.run()
