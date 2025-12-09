import os 

class Config:

    DEBUG_MODE = True

class Paths:

    MAIN_PATH = str(os.path.abspath(__file__)).replace('/config.py','/')
    UPLOADED_FILES = os.path.join(MAIN_PATH,'uploaded_files') + '/'
    LOG_PATH = os.path.join(MAIN_PATH,"logs")
    
    if not os.path.exists(UPLOADED_FILES):
        os.mkdir(UPLOADED_FILES)
    
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)