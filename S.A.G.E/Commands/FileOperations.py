import os
import shutil
from Commands.Voice_utils import speak

def get_default_path():
    """Function to get the default path for file and folder operations"""
    return os.path.join("C:\\Users\\sksha\\OneDrive\\Desktop")

def create_file(file_name, content=""):
    """Function to create a file with specified content"""
    try:
        default_path = get_default_path()
        file_path = os.path.join(default_path, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        speak(f"File {file_name} created successfully.")
    except Exception as e:
        speak(f"Failed to create file {file_name}. Error: {str(e)}")

def delete_file(file_name):
    """Function to delete a file"""
    try:
        default_path = get_default_path()
        file_path = os.path.join(default_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            speak(f"File {file_name} deleted successfully.")
        else:
            speak(f"File {file_name} does not exist in {default_path}")
    except Exception as e:
        speak(f"Failed to delete file {file_name}. Error: {str(e)}")

def create_folder(folder_name):
    """Function to create a folder"""
    try:
        default_path = get_default_path()
        folder_path = os.path.join(default_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        speak(f"Folder {folder_name} created successfully.")
    except Exception as e:
        speak(f"Failed to create folder {folder_name}. Error: {str(e)}")

def delete_folder(folder_name):
    """Function to delete a folder"""
    try:
        default_path = get_default_path()
        folder_path = os.path.join(default_path, folder_name)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            speak(f"Folder {folder_name} deleted successfully.")
        else:
            speak(f"Folder {folder_name} does not exist in {default_path}")
    except Exception as e:
        speak(f"Failed to delete folder {folder_name}. Error: {str(e)}")

def rename_item(source_name, new_name):
    """Function to rename a file or folder"""
    try:
        default_path = get_default_path()
        source_path = os.path.join(default_path, source_name)
        new_path = os.path.join(default_path, new_name)
        if os.path.exists(source_path):
            os.rename(source_path, new_path)
            speak(f"Renamed {source_name} to {new_name} successfully.")
        else:
            speak(f"{source_name} does not exist in {default_path}")
    except Exception as e:
        speak(f"Failed to rename {source_name}. Error: {str(e)}")