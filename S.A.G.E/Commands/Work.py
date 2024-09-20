import os
import time
import cv2
import numpy as np
import pyautogui
import subprocess
import threading
import keyboard
from datetime import datetime
from Commands.Voice_utils import speak

# Global variables
recording = False
out = None

def open_camera_app():
    """Open the Windows Camera app"""
    subprocess.Popen("start microsoft.windows.camera:", shell=True)

def take_photo():
    """Open the Camera app, take a photo, and then close the app"""
    open_camera_app()
    time.sleep(5)  # Wait for the camera app to open
    speak("Say Cheese..")
    pyautogui.press('enter')  # Capture the photo
    time.sleep(2)  # Allow time for the photo to be taken
    pyautogui.hotkey('alt', 'f4')  # Close the Camera app
    speak("Photo taken and saved by Camera app")

def take_screenshot():
    """Take a screenshot and save it to the specified directory"""
    screenshot_path = "C:\\Users\\sksha\\OneDrive\\Desktop\\TRAINING\\Screenshot"
    os.makedirs(screenshot_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = os.path.join(screenshot_path, f"screenshot_{timestamp}.png")

    keyboard.press_and_release('windows+alt+print screen')
    speak(f"Screenshot saved.")

def start_screen_recording():
    """Start recording the screen"""
    global recording, out
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    recording_path = "C:\\Users\\sksha\\OneDrive\\Desktop\\TRAINING\\ScreenRecord"
    os.makedirs(recording_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_file = os.path.join(recording_path, f"recording_{timestamp}.avi")
    out = cv2.VideoWriter(video_file, fourcc, 20.0, (screen_size.width, screen_size.height))
    
    recording = True
    threading.Thread(target=record_screen).start()
    speak(f"Screen recording started.")

def stop_screen_recording():
    """Stop screen recording and release the VideoWriter"""
    global recording, out
    recording = False
    if out:
        out.release()
        out = None
    speak("Screen recording stopped")

def record_screen():
    """Continuously capture the screen and write to the video file"""
    global recording, out
    while recording:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        time.sleep(1 / 20)  # 20 fps