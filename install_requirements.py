"""
This script installs the required packages for movement_detector.py using pip.
Run with: python install_requirements.py
"""
import subprocess
import sys

packages = ["opencv-python", "mss", "numpy", "pytesseract"]

for package in packages:
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
print("All packages installed.")
