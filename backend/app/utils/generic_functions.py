import os
from datetime import datetime

from flask import current_app

def log(msg):

    today = datetime.now()
    date = today.strftime("%d-%m-%Y %H:%M:%S")

    LOG_FILE_FORMAT = f'{date.replace("-","_").split(" ")[0]}.txt'
    LOG_PATH = os.path.join(current_app.config['LOG_PATH'],LOG_FILE_FORMAT)
    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f'{date} {msg} \n')

    log_file.close()

def debug_message(msg,DEBUG_MODE=False) -> None:

    if DEBUG_MODE:
        print(f'\n[DEBUG] {msg}')