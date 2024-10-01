import subprocess

# List of required packages
required_packages = [
    'numpy',
    'sounddevice',
    'pynput',
    'faster-whisper',
    'scipy',
    'deep-translator'
]

def install_package(package):
    """Function to install a Python package via pip."""
    try:
        subprocess.check_call(['pip', 'install', package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {e}")

def check_installation(package):
    """Function to check if a package is installed."""
    try:
        import_module = __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} is not installed. Installing...")
        install_package(package)

def check_tempfile():
    """Function to check if tempfile is available."""
    try:
        import tempfile
        print("tempfile is already available.")
    except ImportError:
        print("tempfile is not available. Installing...")
        install_package('tempfile')  # Note: tempfile is part of Python standard library

def main():
    print("Checking dependencies...")
    for package in required_packages:
        check_installation(package)
    check_tempfile()
    print("Dependencies check complete.")

if __name__ == "__main__":
    main()
