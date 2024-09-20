import time
import pyautogui
from Commands.Voice_utils import speak

def open_whatsapp():
    """Function to open WhatsApp using Windows search"""
    pyautogui.hotkey('win', 's')
    time.sleep(1)  # Allow the search bar to open
    pyautogui.write('WhatsApp')
    time.sleep(1)  # Wait for search results to populate
    pyautogui.press('enter')  # Open WhatsApp
    time.sleep(5)  # Wait for WhatsApp to open fully

def send_whatsapp_message(contact_name, message):
    """Function to send a WhatsApp message"""
    open_whatsapp()
    try:
        pyautogui.hotkey('ctrl', 'f')  # Open the search box
        time.sleep(1)
        pyautogui.write(contact_name)
        time.sleep(2)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')  # Select contact
        time.sleep(2)  # Wait for chat to open
        pyautogui.write(message)  # Type message
        time.sleep(1)
        pyautogui.press('enter')  # Send message
        speak("Message sent successfully.")
    except Exception as e:
        speak(f"Failed to send message: {e}")

def make_call(contact_name):
    """Function to make a WhatsApp call"""
    open_whatsapp()
    try:
        pyautogui.hotkey('ctrl', 'f')  # Open the search box
        time.sleep(1)
        pyautogui.write(contact_name)
        time.sleep(2)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')  # Select contact
        time.sleep(2)  # Wait for chat to open
        # Click the call button (coordinates may need adjustment)
        pyautogui.click(x=1827, y=88)  # Adjust these coordinates based on your screen
        speak("Call initiated.")
    except Exception as e:
        speak(f"Failed to initiate call: {e}")

def make_video_call(contact_name):
    """Function to make a WhatsApp video call"""
    open_whatsapp()
    try:
        pyautogui.hotkey('ctrl', 'f')  # Open the search box
        time.sleep(1)
        pyautogui.write(contact_name)
        time.sleep(2)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')  # Select contact
        time.sleep(2)  # Wait for chat to open
        # Click the video call button (coordinates may need adjustment)
        pyautogui.click(x=1770, y=90)  # Adjust these coordinates based on your screen
        speak("Video call initiated.")
    except Exception as e:
        speak(f"Failed to initiate video call: {e}")