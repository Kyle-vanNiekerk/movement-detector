# Movement Detector for Surveillance Footage

This program allows you to monitor specific areas of surveillance footage for movement, with the assumption that a timestamp is visible somewhere on the footage. It is designed for use with video played back on your screen (e.g., in a browser or video player), and works by capturing the screen region you specify.

## Features
- Interactive selection of the region of interest (ROI) for movement detection.
- Interactive selection of the on-screen timestamp region.
- Uses OCR to extract the timestamp from the footage when movement is detected.
- Logs detected movement events with the extracted timestamp.

## Requirements
- Python 3.8+
- pip packages: `opencv-python`, `mss`, `numpy`, `pytesseract`
- Tesseract OCR (must be installed separately)

## Installation

1. **Clone or download this repository.**

2. **Install Python dependencies:**
   
   Run the following command in the project directory:
   ```sh
   python install_requirements.py
   ```

3. **Install Tesseract OCR:**
   
   - Download the Windows installer from the [Tesseract releases page](https://github.com/tesseract-ocr/tesseract/releases/).
   - Look for the latest `tesseract-ocr-w64-setup-*.exe` file and download it.
   - Run the installer. During installation, check the box to add Tesseract to your system PATH (recommended).
   - By default, Tesseract is installed to `C:\Program Files\Tesseract-OCR`.

   **If you do not add Tesseract to PATH:**
   - Open `movement_detector.py` in a text editor.
   - Uncomment and edit the following line near the top of the file to match your install location:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

## Usage

1. Start playback of your surveillance footage in your preferred video player or browser.
2. Run the program:
   ```sh
   python movement_detector.py
   ```
3. When prompted, select the region of the screen to monitor for movement (drag a rectangle, then press ENTER or SPACE).
4. After a short delay, select the region containing the timestamp (drag a rectangle, then press ENTER or SPACE).
5. The program will monitor the selected area for movement. When movement is detected, it will use OCR to extract the timestamp from the timestamp region and log it to `movement_log.txt`.
6. To stop monitoring, focus the monitoring window and press `q`.

## Notes
- The program works best if the timestamp is clearly visible and not obstructed.
- If OCR accuracy is poor, try adjusting the timestamp region or improving the video quality.
- All movement events are logged in `movement_log.txt` in the project directory.
