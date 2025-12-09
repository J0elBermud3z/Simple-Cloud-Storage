import os
import datetime

from flask import Blueprint, request, jsonify, Response
from flask import current_app

from app.utils.generic_functions import debug_message,log
from app.utils.filesystem import (get_path_size,
                                  get_filetype,
                                  format_root)

from app.decorators.filesystem_validation_decorator import file_validations,folder_validations

file_bp = Blueprint('file', __name__, url_prefix='/api/file') 


@file_bp.route('/', methods=['GET'])
@file_bp.route('/<path:file_name>', methods=['GET'])
@file_validations 
def get_file(file_name: str = '') -> tuple[Response, int]:
    
    base_path = current_app.config['UPLOADED_FILES']    
    final_path = os.path.join(base_path,file_name)
    file_stats = os.stat(final_path)
    return jsonify({
        'status': 'success',
        'data': {
            'name': os.path.basename(final_path),
            'type': get_filetype(final_path),
            'size': get_path_size(final_path),
            'created': datetime.datetime.fromtimestamp(file_stats.st_ctime),
            'last modified': datetime.datetime.fromtimestamp(file_stats.st_ctime),
            'path': format_root(final_path.replace(base_path,''))
            }
        }), 200

@file_bp.route('/', methods=['POST'])
@file_bp.route('/<path:folder_path>', methods=['POST'])
@file_validations
def upload_file(folder_path: str = '', secure_filename: str | None = None) -> tuple[Response, int]: 

    file = request.files['file']
    base_path = current_app.config['UPLOADED_FILES']    
    final_path = os.path.join(base_path,folder_path)

    save_path = (os.path.join(final_path, secure_filename) 
                 if folder_path != '/' 
                 else base_path) 
    
    file.save(save_path)

    return jsonify({
    'status': 'success',
    'data': {
        'name': secure_filename,
        'type': 'file',
        'size': get_path_size(final_path),
        'path': format_root(folder_path)
        }
    }), 201

@file_bp.route('/<path:file_path>', methods=['PATCH'])
@file_validations
def rename_file(file_path: str) -> tuple[Response, int]:
    
    data = request.get_json()
    new_name = data.get('name') 
    
    base_path = current_app.config['UPLOADED_FILES']
    old_path = os.path.join(base_path, file_path)
    directory = os.path.dirname(old_path)
    new_path = os.path.join(directory, new_name)

    try:
        os.rename(old_path, new_path)
        return jsonify({'status':'success',
                        'message': 'File renamed successfully',
                        'data': {'new_name': new_name}
                        }), 200
    
    except Exception as e:
        return jsonify({'status':'error',
                        'message': f'Error renaming file: {str(e)}'
                        }), 500
    
@file_bp.route('/<path:file_path>', methods=['DELETE'])
@file_validations
def delete_file(file_path: str) -> tuple[Response, int]: 

    base_path = current_app.config['UPLOADED_FILES']
    final_file_path = os.path.join(base_path, file_path) 

    try:
        os.remove(final_file_path)
        return jsonify({'status':'success',
                        'message':'File deleted successfully'
                        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error deleting file: {str(e)}'}), 500