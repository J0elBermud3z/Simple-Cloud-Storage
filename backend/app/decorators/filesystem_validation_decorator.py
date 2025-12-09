import os
from pathlib import Path
from functools import wraps

from flask import request, jsonify
from flask import current_app
from werkzeug.utils import secure_filename

from app.utils.generic_functions import debug_message,log
from app.utils.filesystem import secure_path, get_filetype, have_files

def file_validations(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):

        method = request.method
        base_path = current_app.config['UPLOADED_FILES']    
        file_path = kwargs.get('file_path', '') or kwargs.get('file_name', '')
        folder_path = kwargs.get('folder_path', '')

        path_to_check = file_path if file_path else folder_path
        
        if not secure_path(base_path, path_to_check):
             return jsonify({
                "status": "error",
                "message": "Security risk!"
            }), 400

        if method == 'POST':
            if not 'file' in request.files:
                return jsonify({'status':'error', 'message': 'No file selected'}), 400
            
            file = request.files['file']   
            file_name = file.filename
            
            if file_name == '':
                return jsonify({'status':'error', 'message':'Empty filename'}), 400

            kwargs['secure_filename'] = secure_filename(file_name)
            
            final_folder_path = os.path.join(base_path, folder_path)
            if not os.path.isdir(final_folder_path):
                 return jsonify({'status': 'error', 'message': 'Directory not found'}), 404
                 
        if method in ('GET', 'DELETE'):
             final_file_path = os.path.join(base_path, file_path)
             if not os.path.isfile(final_file_path):
                 return jsonify({'status': 'error', 'message': 'File not found'}), 404

        if method == 'PATCH':
             final_file_path = os.path.join(base_path, file_path)
             if not os.path.isfile(final_file_path):
                 return jsonify({'status': 'error', 'message': 'File not found'}), 404
            
             data = request.get_json()
             if not data or not data.get('name'):
                 return jsonify({'status': 'error', 'message': 'New name is required'}), 400
             
             new_name = data.get('name')
             directory = os.path.dirname(final_file_path)
             new_path = os.path.join(directory, new_name)
             
             if os.path.exists(new_path):
                  return jsonify({'status': 'error', 'message': 'File with that name already exists'}), 409
                  
        return func(*args, **kwargs)
    
    return wrapper

def folder_validations(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        method = request.method
        base_path = current_app.config['UPLOADED_FILES']    
        path_arg = kwargs.get('folder_path') or kwargs.get('url', '')
        
        if not secure_path(base_path, path_arg):
             return jsonify({
                "status": "error",
                "message": "Security risk!"
            }), 400
            
        final_path = os.path.join(base_path, path_arg)

        if method == 'POST':

            pass 
            
            if not path_arg:
                 return jsonify({'status': 'error', 'message': "You can't create a folder without a name!"}), 400

        if method == 'GET':
             pass

             if method == 'GET' and not os.path.isdir(final_path):
                 return jsonify({'status': 'error', 'message': 'Directory not found'}), 404

        if method == 'DELETE':
             if not os.path.isdir(final_path):
                 return jsonify({'status': 'error', 'message': 'Directory not found'}), 404

        if method == 'PATCH':
             if not os.path.isdir(final_path):
                 return jsonify({'status': 'error', 'message': 'Directory not found'}), 404
             
             data = request.get_json()
             if not data or not data.get('name'):
                 return jsonify({'status': 'error', 'message': 'New name is required'}), 400

             new_name = data.get('name')
             parent_dir = os.path.dirname(final_path)
             new_path = os.path.join(parent_dir, new_name)

             if os.path.exists(new_path):
                  return jsonify({'status': 'error', 'message': 'Directory with that name already exists'}), 409

        return func(*args, **kwargs)

    return wrapper