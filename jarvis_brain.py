import os, sys
os.chdir(r'/Users/ashokeerthi/TechWorld/PythonWorx/Jarvis_The_Networks_Talker')
sys.path.append(os.getcwd())

from ml_chat_bot import chatbot_response as ml_sentiment
from google_speechRecognition import speech_to_text_google as speech_to_text
from jarvis_speaking import global_call as jarvis_to_speak
from SD_WAN_module import *
from logs import *

user_spoke = None
while not str(user_spoke).lower().__contains__('bye'):
    log_info(f"\n\n{' >==>'*10}")
    log_info('Say Something:\n')
    user_spoke = speech_to_text()
    if user_spoke:
        log_info(f"Recorded:{user_spoke}")
        resp, context = ml_sentiment(user_spoke)
        log_info("{:>100}".format(f'Jarvis: {resp}'))
        jarvis_to_speak(resp)
        if context != "":
            try:
                eval(context)
            except:
                log_info("No proper Contenxt Function defined.")




