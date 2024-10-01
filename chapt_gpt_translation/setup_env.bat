@echo off
:: Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Anaconda is not installed. Please install Anaconda from https://www.anaconda.com/products/distribution and try again.
    exit /b 1
)

:: Create a new conda environment named "transcription_env" if it doesn't exist
echo Checking if conda environment "transcription_env" exists...
conda info --envs | findstr "transcription_env" >nul 2>nul
if %errorlevel% neq 0 (
    echo Creating a new conda environment named "transcription_env"...
    conda create -n transcription_env python=3.8 -y
) else (
    echo Environment "transcription_env" already exists.
)

:: Activate the new environment
echo Activating the environment "transcription_env"...
call conda activate transcription_env

:: Function to check and install pip packages
:check_and_install
pip show %1 >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing %1...
    pip install %1
) else (
    echo %1 is already installed.
)
exit /b 0

:: Install required packages
echo Checking and installing required packages...
call :check_and_install pyaudio
call :check_and_install wave
call :check_and_install SpeechRecognition
call :check_and_install whisper
call :check_and_install openai
call :check_and_install numpy
call :check_and_install tk

echo Setup complete. To activate the environment, use "conda activate transcription_env".
pause
