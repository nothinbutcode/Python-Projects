

# Ensure the script runs with elevated privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script needs to be run as an Administrator."
    Start-Process powershell "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Set execution policy to allow script execution
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Function to check and install AudioDeviceCmdlets module
function Install-AudioDeviceCmdlets {
    if (-not (Get-Module -ListAvailable -Name AudioDeviceCmdlets)) {
        Write-Host "AudioDeviceCmdlets module not found. Installing..."
        Install-Module -Name AudioDeviceCmdlets -Scope CurrentUser -Force
        Write-Host "AudioDeviceCmdlets module installed successfully."
    } else {
        Write-Host "AudioDeviceCmdlets module is already installed."
    }
}

# Function to list audio devices
function List-AudioDevices {
    Write-Host "Listing audio output devices..."
    Get-AudioDevice -List | Where-Object { $_.Type -eq 'Playback' } | Format-Table -Property Name, ID

    Write-Host "Listing audio input devices..."
    Get-AudioDevice -List | Where-Object { $_.Type -eq 'Recording' } | Format-Table -Property Name, ID
}

# Function to set audio devices
function Set-AudioDevices {
    param (
        [string]$InputDevice,
        [string]$OutputDevice
    )

    Write-Host "Setting audio input device to $InputDevice..."
    Set-DefaultAudioDevice -Name $InputDevice -Type 'Recording'

    Write-Host "Setting audio output device to $OutputDevice..."
    Set-DefaultAudioDevice -Name $OutputDevice -Type 'Playback'

    Write-Host "Audio devices have been set."
}

# Check and install AudioDeviceCmdlets module
Install-AudioDeviceCmdlets

# Import the AudioDeviceCmdlets module
Import-Module AudioDeviceCmdlets

# List audio devices
List-AudioDevices

# Prompt user for input and output device names
$inputDevice = Read-Host "Enter the exact name of the audio input device"
$outputDevice = Read-Host "Enter the exact name of the audio output device"

# Set audio devices
Set-AudioDevices -InputDevice $inputDevice -OutputDevice $outputDevice
