import numpy as np
import sounddevice as sd
from  pynput import keyboard
from faster_whisper import WhisperModel
import tempfile
from scipy.io.wavfile import write
import os



class FasterWhisperTranscriber:
    def __init__(self, model_size="large-v3", samplerate=44100):
        self.model_size = model_size
        self.sample_rate = samplerate
        self.model = WhisperModel("large-v3",device="cuda", compute_type="float16")
        self.is_recording = False
        
    def on_press(self, key):
        if key == keyboard.Key.space:
            if not self.is_recording:
                self.is_recording = True
                print("Recording started...")
    
    def on_release(self, key):
        if key == keyboard.Key.space:
            if self.is_recording:
                self.is_recording = False
                print("Stopped recording.")
                return False
    
    def record_audio(self):
        recording = np.array([], dtype="float64").reshape(0,2)
        frames_per_buffer = int(self.sample_rate * 0.1)
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while True:
                if self.is_recording:
                    chunk = sd.rec(frames_per_buffer, samplerate=self.sample_rate,channels=2,dtype="float64")
                    sd.wait()
                    recording = np.vstack([recording,chunk])
                if not self.is_recording and len(recording) > 0:
                    break
            listener.join()
            
        return recording
    
    def save_temp_audio(self, recording):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        write(temp_file.name, self.sample_rate, recording)
        return temp_file.name
    
    def transcribe_audio(self,file_path):
        segments, info = self.model.transcribe(file_path,beam_size=5)
        print("detected lanugage '%s'" % (info.language))
        full_transcription = ""
        for segment in segments:
            print(segment.text)
            full_transcription += segment.text + ""
        os.remove(file_path)
        return full_transcription
    
    def run(self):
        print("Hold spacebar to record")
        while True:
            recording = self.record_audio()
            file_path = self.save_temp_audio(recording)
            self.transcribe_audio(file_path)
            print("\n Press the spacebar to start recording again, or press Clrl+c to exit.")


if __name__ == "__main__":
    transcriber = FasterWhisperTranscriber()
    transcriber.run()                                                                                                                                                                                  
    
            
        
        
       

   