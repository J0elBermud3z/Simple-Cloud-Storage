import os 

class Config:

    DEBUG_MODE = True

class Paths:

    MAIN_PATH = str(os.path.abspath(__file__)).replace('/config.py','/')
    UPLOADED_FILES = os.path.join(MAIN_PATH,'uploaded_files') + '/'
    
    if not os.path.exists(UPLOADED_FILES):
        os.mkdir(UPLOADED_FILES)
    
