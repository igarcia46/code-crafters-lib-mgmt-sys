# Build script for Windows using PyInstaller
# Usage: Run from project root in PowerShell
# Requires: Python installed

$ErrorActionPreference = 'Stop'

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip pyinstaller

# Build a one-directory bundle and include the `data` folder next to the exe
pyinstaller --noconsole --onedir --add-data "data;data" --name BookVault main.py

# Zip the output folder for a GitHub release
if (Test-Path "dist\BookVault") {
    if (Test-Path "dist\BookVault.zip") { Remove-Item "dist\BookVault.zip" }
    Compress-Archive -Path "dist\BookVault\*" -DestinationPath "dist\BookVault.zip"
    Write-Host "Created dist\\BookVault.zip - upload this to GitHub Releases"
} else {
    Write-Error "Build failed: dist\BookVault not found."
}
