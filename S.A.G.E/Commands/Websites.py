import subprocess
from Commands.Voice_utils import speak

# Dictionary of websites
websites_dict = {
    "google": "https://www.google.com/",
    "gmail": "https://mail.google.com/mail/u/0/#inbox",
    "github": "https://github.com/",
    "youtube": "https://www.youtube.com/",
    "hackerrank": "https://www.hackerrank.com/dashboard",
    "hackerearth": "https://www.hackerearth.com/challenges/",
    "codeforces": "https://codeforces.com/enter?back=%2Fproblemset",
    "codechef": "https://www.codechef.com/",
    "codecademy": "https://www.codecademy.com/catalog",
    "leetcode": "https://leetcode.com/",
    "udemy": "https://www.udemy.com/",
    "edx": "https://www.edx.org/",
    "coursera": "https://www.coursera.org/",
    "w3resource": "https://www.w3resource.com/",
    "w3schools": "https://www.w3schools.com/",
    "geeksforgeeks": "https://www.geeksforgeeks.org/",
    "stackoverflow": "https://stackoverflow.com/",
    "instagram": "https://www.instagram.com/?hl=en",
    "facebook": "https://www.facebook.com/",
    "linkedin": "https://www.linkedin.com/",
    "twitter": "https://twitter.com/LOGIN",
    "imdb": "https://imdb.com/",
    "netflix": "https://netflix.com/",
    "amazon prime": "https://primevideo.com/",
    "whatsapp": "https://web.whatsapp.com/",
    "hotstar": "https://www.hotstar.com/",
    "cricbuzz": "https://www.cricbuzz.com/",
    "google maps": "https://maps.google.com/",
    "flipkart": "https://www.flipkart.com/",
    "amazon": "https://www.amazon.com/",
    "nykaa": "https://www.nykaa.com/",
    "myntra": "https://www.myntra.com/",
    "amazon flex": "https://flex.amazon.in/",
    "swiggy": "https://www.swiggy.com/",
    "zomato": "https://www.zomato.com/",
    "spotify": "https://open.spotify.com/"
}

def open_chrome(url):
    """Function to open a URL in Chrome"""
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    subprocess.run([chrome_path, url])

def open_website(website_name):
    """Function to open a website based on user input"""
    url = websites_dict.get(website_name.lower())
    if url:
        speak(f"Opening {website_name}...")
        open_chrome(url)
    else:
        speak(f"Website '{website_name}' not found in the list.")

def search_google(query):
    """Function to search Google"""
    speak("Wait a minute sir..")
    open_chrome(f"https://www.google.com/search?q={query}")

def search_youtube(query):
    """Function to search YouTube"""
    speak("Wait a minute sir..")
    open_chrome(f"https://www.youtube.com/results?search_query={query}")