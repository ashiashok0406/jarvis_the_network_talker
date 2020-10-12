
from gtts import gTTS
import pygame
import os

audioFileSavePath = 'textToRead.mp3'

# Playing above created file
from pygame import mixer

def create_mp3_file_for_given_text(inputText):
    lang = 'en'

    speech = gTTS(text=inputText, lang=lang, slow=False)
    speech.save(audioFileSavePath)
    return True

def play_saved_file():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audioFileSavePath)
    pygame.mixer.music.play()
    # pygame.event.wait()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    return True

def global_call(text_to_play):
    create_mp3_file_for_given_text(text_to_play)
    play_saved_file()

if __name__ == "__main__":
    global_call('Following is the list of alarms observed on the network')
