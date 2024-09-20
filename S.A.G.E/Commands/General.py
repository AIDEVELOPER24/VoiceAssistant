import requests
import datetime
import pyjokes
import time
import random
from Commands.Voice_utils import speak, takeCommand

# API Keys
NEWS_API_KEY = "c548425148dd4c51a40e0e535d0b1f87"
WEATHER_API_KEY = "82d0ab6cdee30f8b0462769ceeaba970"
GEOLOCATION_API_KEY = "6dad3741e6c64bb2beab64f66346554a"

def get_current_location():
    """Function to get current location using geolocation API"""
    url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={GEOLOCATION_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        location_data = response.json()
        city = location_data['city']
        country_code = location_data['country_code'].lower()
        return city, country_code
    else:
        speak("Error fetching current location.")
        return None, None

def get_news(region=None, count=5):
    """Function to get news headlines"""
    if not region:
        location = get_current_location()
        region = location[1] if location else None
        if not region:
            return None
    url = f"https://newsapi.org/v2/top-headlines?country={region}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    random.shuffle(articles)  # Shuffle the articles to ensure randomness
    articles = articles[:count]
    news_list = [article["title"] for article in articles]
    for news in news_list:
        speak(news)
    return news_list

def get_weather(city=None):
    """Function to get current weather"""
    if not city:
        location = get_current_location()
        city = location[0] if location else None
        if not city:
            return None
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if 'main' in response and 'weather' in response:
        weather = f"Current temperature in {city} is {response['main']['temp']}°C with {response['weather'][0]['description']}."
        speak(weather)
        return weather
    else:
        speak(f"Error fetching weather for {city}.")
        return None

def tell_joke():
    """Function to tell a joke"""
    joke = pyjokes.get_joke()
    speak(joke)
    return joke

reminders = []

def set_reminder(reminder_text):
    """Function to set a reminder"""
    reminders.append((reminder_text, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    speak("Reminder saved.")
    return reminders

def get_reminders():
    """Function to get all reminders"""
    if not reminders:
        speak("You have no reminders.")
        return []
    speak("Here are your reminders:")
    for reminder in reminders:
        speak(reminder[0])
    return reminders

def set_timer():
    """Function to set a timer"""
    while True:
        G3 = ["For how many seconds should I set the timer?",
              "Please tell me the duration for the timer.", 
              "How long should the timer be set for?", 
              "Tell me the number of seconds for the timer.", 
              "What duration should I set the timer to?", 
              "How many seconds do you want the timer for?",
              "What should be the timer's duration?",
              "How long do you need the timer to run?"]
        speak(random.choice(G3))
        duration_input = takeCommand()
        
        try:
            duration = int(duration_input)
            speak(f"Setting a timer for {duration} seconds.")
            time.sleep(duration)
            speak("Time's up!")
            break
        except ValueError:
            speak("Sorry, I didn't get the time duration. Please provide a valid number of seconds.")

def lookup_word(word):
    """Function to look up the definition of a word"""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url).json()
    if response:
        definition = response[0]["meanings"][0]["definitions"][0]["definition"]
        speak(f"{word} means {definition}.")
        return definition
    else:
        speak("Error looking up the word.")
        return None

def get_random_funfact():
    """Function to get a random fun fact"""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url).json()
    if response:
        funfact = response["text"]
        speak(funfact)
        return funfact
    else:
        speak("Error fetching fun fact.")
        return None