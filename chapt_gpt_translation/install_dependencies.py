import subprocess
import sys

def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name, command):
    try:
        if not is_package_installed(package_name):
            print(f"Installing {package_name}...")
            subprocess.check_call(command, shell=True)
        else:
            print(f"{package_name} is already installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package_name}: {e}")

def main():
    # Check and install packages
    install_package("torch", "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    install_package("whisper", "pip install git+https://github.com/openai/whisper.git")
    install_package("pyaudio", "pip install pyaudio")
    install_package("tkinter", "pip install python-tk")
    install_package("speech_recognition", "pip install SpeechRecognition")
    install_package("numpy", "pip install numpy")

if __name__ == "__main__":
    main()
