import streamlit as st
import speech_recognition as sr
import pyttsx3
import pywhatkit as kit
import datetime
import wikipedia
import threading

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to listen for voice input
def listen():
    try:
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = r.listen(source, phrase_time_limit=5)
            query = r.recognize_google(audio, language='en-US')
            st.write(f"User said: {query}")
            return query
    except sr.UnknownValueError:
        st.write("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        st.write("Error requesting results.")
        return None

# Define a function to respond to voice input
def respond(query):
    if query is None:
        return

    # Basic commands
    if "hello" in query.lower():
        response = "Hello! How can I assist you?"
    elif "what's your name" in query.lower():
        response = "I'm your voice assistant."
    elif "time" in query.lower():
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}."
    elif "search" in query.lower():
        query = query.replace("search", "").strip()
        kit.search(query)
        response = f"Searching for {query}..."
    else:
        try:
            response = wikipedia.summary(query, sentences=2)
        except wikipedia.exceptions.DisambiguationError:
            response = "Too many results. Please be more specific."
        except wikipedia.exceptions.PageError:
            response = "No results found."

    # Display response in chat
    st.write("Bot:", response)

    # Speak response
    def speak_response():
        engine.say(response)
        engine.runAndWait()

    threading.Thread(target=speak_response).start()

# Create a Streamlit app
st.title("Voice Assistant")

# Initialize variables
query_list = []

# Create a chat interface
st.write("Chat with me!")
user_input = st.text_area("You:", height=100)

# Create buttons
col1, col2 = st.columns(2)

if col1.button("Listen"):
    query = listen()
    if query is not None:
        query_list.append(query)
        respond(query)

if col2.button("Send"):
    if user_input:
        respond(user_input)

if st.button("Stop"):
    if len(query_list) > 0:
        for query in query_list:
            respond(query)
        query_list = []
        st.write("All queries responded to.")
    else:
        st.write("No queries to respond to.")

# Add some CSS to make the interface more attractive
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}

.stTextArea>div>textarea {
    width: 100%;
    height: 100px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.stButton>button {
    width: 100%;
    height: 40px;
    padding: 10px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    background-color: #4CAF50;
    color: #fff;
    cursor: pointer;
}

.stButton>button:hover {
    background-color: #3e8e41;
}
</style>
""", unsafe_allow_html=True)