import speech_recognition as sr
import sys, os
from logs import *

def speech_to_text_google():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            # print("Say Something: ")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            # print(f"Recorded\n:{text}")
        except:
            # print("Waiting for your voice. If done, say 'bye'")
            return None

    return text

if __name__ == "__main__":
    speech_to_text_google()