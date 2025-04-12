from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import pywhatkit as kit
import datetime
import wikipedia

app = Flask(__name__)

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to listen for voice input
def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=5)
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
            return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        print("Error requesting results.")
        return None

# Define a function to respond to voice input
def respond(query):
    if query is None:
        return

    # Basic commands
    if "hello" in query.lower():
        engine.say("Hello! How can I assist you?")
    elif "what's your name" in query.lower():
        engine.say("I'm your voice assistant.")
    elif "time" in query.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        engine.say(f"The current time is {current_time}.")
    elif "search" in query.lower():
        query = query.replace("search", "").strip()
        kit.search(query)
        engine.say(f"Searching for {query}...")
    elif "wikipedia" in query.lower():
        query = query.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            engine.say(result)
        except wikipedia.exceptions.DisambiguationError:
            engine.say("Too many results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            engine.say("No results found.")

    # Run the response
    engine.runAndWait()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listen", methods=["POST"])
def listen_route():
    query = listen()
    respond(query)
    return "Listening..."

if __name__ == "__main__":
    app.run(debug=True)