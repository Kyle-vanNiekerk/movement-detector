# Movement Detector for Screen Region (Edge Browser)
# Requirements: opencv-python, mss, numpy
# Usage:
# 1. Run this script while your video is playing in Edge (Explorer mode).
# 2. On first run, select the region of interest (ROI) with your mouse.
# 3. The script will monitor that region for significant movement and log timestamps.

import cv2
import numpy as np
import mss
import time
import pytesseract

# If Tesseract is not in PATH, set the following to its full path (e.g., r'C:\Program Files\Tesseract-OCR\tesseract.exe')
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- CONFIGURABLE PARAMETERS ---
# How sensitive? (higher = less sensitive)
MOVEMENT_THRESHOLD = 5000  # Number of changed pixels to trigger event
# How often to check (seconds)
FRAME_INTERVAL = 0.2


# --- ROI SELECTION ---
def select_roi_from_screen(prompt="Select ROI"):
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        print(f"{prompt} (drag rectangle, then press ENTER or SPACE)")
        roi = cv2.selectROI(prompt, screenshot, False, False)
        cv2.destroyWindow(prompt)
        x, y, w, h = roi
        if w == 0 or h == 0:
            raise Exception("ROI selection cancelled or invalid.")
        return {'top': y, 'left': x, 'width': w, 'height': h}

# --- MOVEMENT DETECTION ---

def main():
    print("Starting movement detector...")
    roi = select_roi_from_screen("Select MOVEMENT ROI")
    print(f"Monitoring region: {roi}")
    print("Waiting 2 seconds before timestamp ROI selection...")
    time.sleep(2)
    timestamp_roi = select_roi_from_screen("Select TIMESTAMP ROI")
    print(f"Timestamp region: {timestamp_roi}")

    with mss.mss() as sct:
        prev_gray = None
        log_file = open("movement_log.txt", "a")
        try:
            while True:
                img = np.array(sct.grab(roi))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                if prev_gray is None:
                    prev_gray = gray
                    time.sleep(FRAME_INTERVAL)
                    continue
                # Frame difference
                frame_delta = cv2.absdiff(prev_gray, gray)
                thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                changed = np.sum(thresh > 0)
                if changed > MOVEMENT_THRESHOLD:
                    # Grab timestamp region and OCR it
                    ts_img = np.array(sct.grab(timestamp_roi))
                    ts_img_gray = cv2.cvtColor(ts_img, cv2.COLOR_BGR2GRAY)
                    ts_img_gray = cv2.threshold(ts_img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                    ocr_text = pytesseract.image_to_string(ts_img_gray, config='--psm 7').strip()
                    print(f"Movement detected at '{ocr_text}' (pixels changed: {changed})")
                    log_file.write(f"{ocr_text} - Movement detected (pixels changed: {changed})\n")
                    log_file.flush()
                prev_gray = gray
                # Optional: show live view
                cv2.imshow("Monitoring", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                time.sleep(FRAME_INTERVAL)
        finally:
            log_file.close()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
