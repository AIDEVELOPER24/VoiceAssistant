import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Ensure correct voice index
engine.setProperty('rate', 150)

def speak(audio):
    """Function to make the assistant speak"""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Function to take voice commands from the user"""
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