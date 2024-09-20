import pyautogui
import subprocess
import time
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from Commands.Voice_utils import speak, takeCommand

# Volume Controls
def volume_up(steps=5):
    """Increase system volume"""
    for i in range(steps):
        pyautogui.press("volumeup")

def volume_down(steps=5):
    """Decrease system volume"""
    for i in range(steps):
        pyautogui.press("volumedown")

def normalize_volume():
    """Set volume to 50%"""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    
    target_volume = 50
    if current_volume < target_volume:
        for level in range(int(current_volume), target_volume + 1):
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            time.sleep(0.01)
        speak("Volume is at 50%")
    elif current_volume > target_volume:
        for level in range(int(current_volume), target_volume - 1, -1):
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            time.sleep(0.01)
        speak("Volume is at 50%")
    else:
        speak("Volume is already at 50%")

def mute_volume():
    """Mute system volume"""
    pyautogui.press("volumemute")

def unmute_volume():
    """Unmute system volume"""
    pyautogui.press("volumemute")  # Toggle mute

# Tab Management
def switch_tab():
    """Switch to the next browser tab"""
    pyautogui.hotkey('ctrl', 'tab')

def new_tab():
    """Open a new browser tab"""
    pyautogui.hotkey('ctrl', 't')

def close_tab():
    """Close the current browser tab"""
    pyautogui.hotkey('ctrl', 'w')

# Window Management
def minimize_window():
    """Minimize the current window"""
    pyautogui.hotkey('win', 'down')

def maximize_window():
    """Maximize the current window"""
    pyautogui.hotkey('win', 'up')

def switch_window():
    """Switch between open windows"""
    pyautogui.hotkey('alt', 'tab')

# Edit Functions
def take_note():
    """Open Notepad and take a note"""
    subprocess.Popen(['notepad.exe'])
    time.sleep(1)  # Wait for Notepad to open
    note = takeCommand()
    time.sleep(1)  # Wait to ensure Notepad is active
    write_text(note)

def write_text(text):
    """Write text to the active window"""
    pyautogui.write(text, interval=0.1)

def select_all():
    """Select all text"""
    pyautogui.hotkey('ctrl', 'a')

def enter():
    """Press Enter key"""
    pyautogui.press('enter')

def delete_text():
    """Delete text"""
    pyautogui.press('backspace')

def copy_text():
    """Copy selected text"""
    pyautogui.hotkey('ctrl', 'c')

def cut_text():
    """Cut selected text"""
    pyautogui.hotkey('ctrl', 'x')

def paste_text():
    """Paste copied or cut text"""
    pyautogui.hotkey('ctrl', 'v')

def undo():
    """Undo last action"""
    pyautogui.hotkey('ctrl', 'z')

def redo():
    """Redo last undone action"""
    pyautogui.hotkey('ctrl', 'y')

# Swipe Functions
def swipe_up():
    """Scroll up"""
    pyautogui.scroll(500)

def swipe_down():
    """Scroll down"""
    pyautogui.scroll(-500)

# System Tasks
def turn_off_screen():
    """Turn off the screen (Windows only)."""
    speak("turning off the screen..")
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)

def shutdown_system():
    """Shutdown the system"""
    speak("Shutting down the system..")
    subprocess.run(['shutdown', '/s', '/t', '0'])

def restart_system():
    """Restart the system"""
    speak("Restarting the system..")
    subprocess.run(['shutdown', '/r', '/t', '0'])