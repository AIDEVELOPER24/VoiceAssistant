import pyautogui
import time

def open_application(app_name):
    # Open the search bar
    pyautogui.hotkey('win', 's')
    time.sleep(1)  # Wait for the search bar to open

    # Type the application name
    pyautogui.write(app_name, interval=0.1)
    time.sleep(1)  # Wait for the search results

    # Press Enter to open the application
    pyautogui.press('enter')
    time.sleep(5)  # Wait for the application to open

def close_application():
    # Close the current application
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)  # Wait for the application to close