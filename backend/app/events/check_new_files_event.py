import threading
import time

from flask import current_app
from flask import request

from app.extensions.ext import socketio
from app.utils.functions import debug_message
from app.utils.filesystem import get_total_files_and_directories


def check_files_thread(app, sid):
    with app.app_context():
        base_path = current_app.config['UPLOADED_FILES']
        aux_new_files = get_total_files_and_directories(base_path)

        while True:
            time.sleep(1)
            new_files = get_total_files_and_directories(base_path)

            if new_files != aux_new_files:
                aux_new_files = new_files
                socketio.emit('new_files', {'message': 'new change detected'}, to=sid)

            debug_message('[*] [EVENT] [check_new_files_event] running...',DEBUG_MODE=current_app.config['DEBUG_MODE'])

@socketio.on('connect')
def on_connect():
    sid = request.sid
    app = current_app._get_current_object()

    thread = threading.Thread(
        target=check_files_thread,
        args=(app, sid)
    )
    thread.daemon = True
    thread.start()
