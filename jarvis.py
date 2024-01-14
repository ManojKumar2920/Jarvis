import pyttsx3 as tts
import speech_recognition as sr
import subprocess
import webbrowser
import datetime
import time
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import google.generativeai as genai

engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

SPOTIPY_CLIENT_ID = 'your-client-id'
SPOTIPY_CLIENT_SECRET = 'your-client-secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:3000'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read user-read-playback-state user-modify-playback-state"))

GOOGLE_API_KEY= 'your-api-key'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetings():
    print("Welcome back sir!")
    speak("Welcome back sir!")
    print("Jarvis at your service! ")
    speak("Jarvis at your service!")

def date_time():
    now = datetime.datetime.now()
    date_time_str = now.strftime("%B %d, %Y %I:%M %p")  # Format as "Month Day, Year Hour:Minute AM/PM"
    print(f"The current date and time is {date_time_str}")
    speak(f"The current date and time is {date_time_str}")

def search(command):
    search_query = command.replace('search', '')
    url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {search_query}.")
    
def play_song(command):
    song_name = command.replace('play', '')
    results = sp.search(q=song_name, type='track', limit=1)

    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id'] 
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri], device_id=device_id)
        speak(f"Now playing {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}.")
    else:
        try:
            subprocess.Popen(["spotify"])
        except FileNotFoundError:
            speak("Spotify is not installed on this system.")

        time.sleep(5)

        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            track_uri = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=[track_uri], device_id=device_id)
            speak(f"Now playing {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}.")
        else:
            speak("No active devices found!")


def speak_lines(text, num_lines=3):
    lines = text.split('\n')[:num_lines]
    final_text = ' '.join(lines)
    engine.say(final_text)
    engine.runAndWait()       

def geminiai(command):
    print('Please wait sir..!')
    speak('Please wait sir..!')
    response = model.generate_content(command)
    response_text = response.text
    print(response_text)
    speak_lines(response_text)


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language="en-in")
        print("User: ",command)

    except Exception as e:
        print(e)
        speak("Please say that again")
        return "Try Again"

    return command

if __name__ == "__main__":
    greetings()
    while True:
        command_text = command().lower()
        
        if 'who are you' in command_text:
            print("I'm Jarvis! Virtual assistant developed by Manoj Kumar.")
            speak("I'm Jarvis! Virtual assistant developed by Manoj Kumar.")
            
        elif 'hey jarvis' in command_text:
            print("Yes sir, I'm happy to see you!")
            speak("Yes sir, I'm happy to see you!")
            
        elif 'how are you' in command_text:
            print("Great! How about you sir ?")
            speak("Great! How about you sir ?")
            
        elif 'fine' in command_text or 'good' in command_text or 'great' in command_text:
            print("Glad to hear this, How can i help you sir ?")    
            speak("Glad to hear this, How can i help you sir ?")
            
        elif 'not so well' in command_text:
            print("Sorry sir, how can i help you to made the day better?")
            speak("Sorry sir, how can i help you to made the day better?")
        
        elif 'date' in command_text or 'time' in command_text:
            date_time()

        elif 'search' in command_text:
            search(command_text)
        
        elif 'play' in command_text:
            play_song(command_text)
        
        elif 'quit' in command_text or 'exit' in command_text or 'go offine' in command_text:
            speak('GoodBye Sir!')
            print('GoodBye Sir!')
            exit()
        
        else:
            geminiai(command_text)
