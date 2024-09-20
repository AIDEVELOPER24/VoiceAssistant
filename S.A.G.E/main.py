from datetime import datetime
import pyttsx3
import speech_recognition as sr
import eel
import sqlite3
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import random
import re


# Importing command modules
from Commands.AppTask import *
from Commands.FileOperations import *
from Commands.Games import *
from Commands.General import *
from Commands.SystemTask import *
from Commands.Websites import *
from Commands.Whatsapp import *
from Commands.Work import *

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Select the voice (index 0 is typically the default)
engine.setProperty('rate', 200) # Set the speech rate

# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
conn.commit()

# Initialize Eel
eel.init('web')

# Global variables for hold and timer
on_hold = True
last_interaction_time = datetime.now()
hold_threshold = 10  # seconds
logged_in_username = None

def reset_timer():
    global last_interaction_time
    last_interaction_time = datetime.now()

# Function to validate email addresses
def is_valid_gmail(email):
    """Check if the provided email is a valid Gmail address."""
    # Regex pattern for Gmail validation
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if re.match(pattern, email):
        return True
    else:
        return False

@eel.expose
def registeruser(email, username, password):
    """Register a new user, allowing only @gmail.com addresses."""
    if not is_valid_gmail(email):
        speak("Please use a valid Gmail address to register.")
        return False

    try:
        cursor.execute('INSERT INTO users (email, username, password) VALUES (?,?,?)',
                       (email, username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Handle duplicate username or email
        return False

@eel.expose
def loginuser(username, password):
    """Login an existing user"""
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        global logged_in_username
        logged_in_username = username
        return True
    else:
        return False
    
@eel.expose
def logoutuser():
    """Logout the current user and navigate to the login page"""
    global logged_in_username
    logged_in_username = None

    
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_user_name(username):
    """Retrieve the name of the logged-in user from the database."""
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def WishMe():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good Morning! {logged_in_username}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon! {logged_in_username}")
    else:
        speak(f"Good Evening! {logged_in_username}")
    assname = "Sage 1.0"
    if logged_in_username:
        speak(f", I am a Voice Assistant {assname}, and I am here to listen and complete your work with your voice commands.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("....")
        return "None"
    return query

def wake_word(word="Sage"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("..........")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        if word.lower() in query.lower():
            print(f"Wake word detected: {query}")
            return True
        else:
            print(f"Wake word not detected: {query}")
            return False
    except Exception as e:
        return False
    
# Load the trained model
model_path = 'my_model.keras'
model = tf.keras.models.load_model(model_path)

# Load the tokenizer
tokenizer_path = 'tokenizer.pickle'
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the label encoder
label_encoder_path = 'label_encoder.pickle'
with open(label_encoder_path, 'rb') as ecn_file:
    label_encoder = pickle.load(ecn_file)

# Function to preprocess and predict intent
def predict_intent(query):
    max_len = 30
    sequence = tokenizer.texts_to_sequences([query])
    padded_sequence = pad_sequences(sequence, truncating='post', maxlen=max_len)
    prediction = model.predict(padded_sequence)
    predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])
    return predicted_label[0]

@eel.expose
def start_assistant():
    global on_hold
    WishMe()
    on_hold = False

    while True:
        if on_hold:
            if wake_word():
                speak("I am Listening, sir!")
                reset_timer()
                on_hold = False
        else:
            query = takeCommand().lower()
            intent = predict_intent(query)
            if query == "none":
                if (datetime.now() - last_interaction_time).seconds > hold_threshold:
                    on_hold = True
                continue

            reset_timer()

            # Process commands based on the detected intent
            if intent == "greeting":
                speak("Hello sir, How can i hel you today?")

            elif "what is my name" in query:
                if logged_in_username:
                    user_name = get_user_name(logged_in_username)
                    if user_name:
                        speak(f"Your name is {user_name}.")
                    else:
                        speak("I'm sorry, I could not retrieve your name.")
                else:
                    speak("You are not logged in, so I don't know your name.")

            elif "who are you" in query.lower():
                speak('My name is Sage. I can perform a variety of tasks as programmed by my creator.')

            elif "who created you" in query.lower():
                speak('I am created by an anonymous coder to perform a variety of tasks.')

            elif "whats your full form" in query.lower() or "your full form" in query.lower():
                speak('Smart Assistant for Greater Efficiency')

            elif intent == "open_application":
                app_name = query.split("open", 1)[1].strip()
                speak(f"Opening {app_name}")
                open_application(app_name)

            elif intent == "close_application":
                speak("Closing the current application")
                close_application()

            elif intent == "create_file":
                F1 = ["What should be the name of the file?", 
                            "Please tell the file name.", 
                            "What's the file name?"]
                speak(random.choice(F1))
                file_name = takeCommand().strip()
                F2 = ["What's the content of a file?", 
                        "Please provide the content."]
                speak(random.choice(F2))
                content = takeCommand().strip()
                create_file(file_name, content)
                
            elif intent == "delete_file":
                F3 = ["What is the name of a file to delete?", 
                            "Please tell the file name.", 
                            "What's the file name?"]
                speak(random.choice(F3))
                file_name = takeCommand().strip()
                delete_file(file_name)
                
            elif intent == "create_folder":
                F4 = ["What should be the name of a folder?", 
                            "Please tell the folder name.", 
                            "What's the folder name?"]
                speak(random.choice(F4))
                folder_name = takeCommand().strip()
                create_folder(folder_name)
                
            elif intent == "delete_folder":
                F5 = ["What is the name of the folder to delete?", 
                            "Please tell the folder name.", 
                            "What's the folder name?"]
                speak(random.choice(F5))
                folder_name = takeCommand().strip()
                delete_folder(folder_name)

            elif intent == "rename_item":
                speak("What is the current name of the item?")
                source_name = takeCommand().strip()
                speak("What should be the new name of the item?")
                new_name = takeCommand().strip()
                rename_item(source_name, new_name)

            elif intent == "start_game":
                start_game()
        
            elif intent == "get_news":
                G1 = ["Wait a minute sir.", 
                      "One minute", 
                      "Okay sir, wait a moment..",
                      "Just a moment please.",
                      "Give me a second to fetch that.",
                      "I'll have the news for you shortly."]
                speak(random.choice(G1))
                get_news()

            elif intent == "get_weather":
                G2 = ["Getting the weather report...",
                      "Hold on a minute..",
                      "Fetching the latest weather update...",
                      "Please wait a moment while I get the weather details.",
                      "Just a second, getting the weather info.",
                      "I'll have the weather report for you shortly."]
                speak(random.choice(G2))
                get_weather()

            elif intent == "tell_joke":
                tell_joke()

            elif intent == "set_reminder":
                set_reminder(query.replace("remind me", "").strip())

            elif intent == "get_reminders":
                get_reminders()
                
            elif intent == "set_timer":
                set_timer()
                
            elif intent == "lookup_word":
                lookup_word(query.replace("define", "").strip())

            elif intent == "get_random_funfact":
                get_random_funfact()

            elif intent == "volume_up":
                volume_up()
    
            elif intent == "volume_down":
                volume_down()
    
            elif intent == "mute_volume":
                mute_volume()
    
            elif intent == "unmute_volume":
                unmute_volume()

            elif intent == "normalize_volume" in query:
                normalize_volume()
    
            elif intent == "switch_tab" in query:
                switch_tab()
    
            elif intent == "new_tab" in query:
                new_tab()
    
            elif intent == "close_tab" in query:
                close_tab()
    
            elif intent == "switch_window" in query:
                switch_window()
    
            elif intent == "minimize_window":
                minimize_window()
    
            elif intent == "maximize_window":
                maximize_window()
    
            elif intent == "take_note" in query:
                take_note()
    
            elif intent == "select_all" in query:
                select_all()

            elif intent == "delete_text" in query:
                delete_text()

            elif intent == "copy_text" in query:
                copy_text()

            elif intent == "cut_text" in query:
                cut_text()

            elif intent == "paste_text" in query:
                paste_text()

            elif intent == "undo" in query:
                undo()

            elif intent == "redo" in query:
                redo()

            elif intent == "swipe_up" in query:
                swipe_up()

            elif intent == "swipe_down":
                swipe_down()

            elif intent == "turn_off_screen":
                turn_off_screen()

            elif intent == "shutdown_system":
                shutdown_system()

            elif intent == "restart_system":
                restart_system()

            elif intent == "open_website":
                website_name = query.lower().replace("open website", "").strip()
                open_website(website_name)
    
            elif intent == "search_google":
                G4 = ["What should I search on Google?", 
                      "Please tell me what to search on Google.", 
                      "What do you want to search for on Google?",
                      "Can you specify what to search on Google?", 
                      "What would you like me to look up on Google?"]
                speak(random.choice(G4))
                search_query = takeCommand().strip()
                search_google(search_query)
    
            elif intent == "search_youtube":
                Y1 = ["What should I search on YouTube?", 
                      "Please tell me what to search on YouTube.", 
                      "What do you want to search for on YouTube?",
                      "Can you specify what to search on YouTube?", 
                      "What would you like me to look up on YouTube?",
                      "What video you want to see?"]
                speak(random.choice(Y1))
                search_query = takeCommand().strip()
                search_youtube(search_query)

            elif intent == "send_whatsapp_message":
                speak("Please provide the recipient's name.")
                contact_name = takeCommand()
                speak("What's the message?")
                message_content = takeCommand()
                send_whatsapp_message(contact_name, message_content)
    
            elif intent == "make_call":
                speak("Please provide the recipient's name.")
                contact_name = takeCommand()
                make_call(contact_name)
    
            elif intent == "make_video_call":
                speak("Please provide the recipient's name.")
                contact_name = takeCommand()
                make_video_call(contact_name)

            elif intent == 'take_photo':
                take_photo()

            elif intent == 'take_screenshot':
                take_screenshot()

            elif intent == 'start_screen_recording':
                start_screen_recording()

            elif intent == 'stop_screen_recording':
                stop_screen_recording()

            elif intent == "thanks":
                speak("You're Welcome!")

            elif intent == "bye":
                speak("Bye sir, Have a good day.")
                break

if __name__ == "__main__":
    eel.start('page-1.html', size=(1500, 1500))