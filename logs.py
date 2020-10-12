import os
import logging
import datetime
from pathlib import Path

logfilepath = Path('.').joinpath('logs')
logfilename = logfilepath.joinpath(str(datetime.datetime.now().strftime('%d-%m-%Y %I%M%S')) + '.log')
os.makedirs(logfilepath, mode=0o777, exist_ok=True)
handlers = [logging.FileHandler(logfilename), logging.StreamHandler()]

logging.basicConfig(format='%(message)s',
                    level=logging.INFO,
                    handlers=handlers)
print(f"Logs written into file name: {logfilename}")

def log_warning(message):
    logging.warning(f'\n{message}')

def log_info(message):
    logging.info(f'\n{message}')

def log_error(message):
    logging.error(f'\n{message}')
