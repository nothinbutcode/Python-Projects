
import wave
import sounddevice as sd

# Audio file formats
# .mp3
#.flac
#.wav

# Audio signal parameters
# - number of  channels: mono = 1 , sterio = 2 indipend
# - sample width: number of bites for each sample
# - framerate/sample_rate:number of samples per sec(most common: 44,100Hz)
# - number of frames
# - values from a frame

# #audio obj
# obj = wave.open("Wave_audio-files\Random_speech.wav", "rb")
# #print audio parameters
# print("number of channels:",obj.getnchannels() )
# print("sample width:",obj.getsampwidth() )
# print("frame rate:",obj.getframerate() )
# print("numberofframes:",obj.getnframes() )
# print("parameters:",obj.getparams() )
# #fromes in audio
# frames = obj.readframes(-1)
# print(type(frames), type(frames[0]))
# print(len(frames))

# # how long the audio = frrate/frnumber
# t_audio = obj.getnframes() / obj.getframerate()

# print("audio is " ,t_audio,"sec long" )
# obj.close()

# #create new obj from sample to manipulate

# obj_new = wave.open("Random_speechnew1.wav", "wb")

# obj_new.setnchannels(2)
# obj_new.setsampwidth(2)
# obj_new.setframerate(44100.0)


# obj_new.writeframes(frames)
# obj_new.close()


def list_audio_devices():
    print("Available audio devices:")
    for i, device in enumerate(sd.query_devices()):
        print(f"  {i}: {device['name']}")

list_audio_devices()




