import os
import shutil


from flask import Blueprint, jsonify, Response, request
from flask import current_app

from app.utils.generic_functions import debug_message,log
from app.utils.filesystem import (have_files,
                                  get_filetype,
                                  get_path_size,
                                  format_root)

from app.decorators.filesystem_validation_decorator import folder_validations

folder_bp = Blueprint('folder', __name__, url_prefix='/api/folder') 

@folder_bp.route('/', methods=['GET'])
@folder_bp.route('/<path:url>', methods=['GET'])
def all_files(url: str = '/') -> tuple[Response, int]:

    base_path = current_app.config['UPLOADED_FILES']
    clean_url = url.strip('/')

    final_path = os.path.join(base_path, clean_url)

    if not os.path.isdir(final_path):
        return jsonify({'status': 'error', 'message': 'Directory not found'}), 404

    all_files_and_directories = {
        'path': url if url == '/' else f"/{clean_url}",
        'files': [],
        'directories': [],
        'size': get_path_size(final_path),
        'actions': []
    }

    all_files_and_directories['files'] = [
        {
            'name': f,
            'type': get_filetype(os.path.join(final_path, f))
        }
        for f in os.listdir(final_path)
        if os.path.isfile(os.path.join(final_path, f))
    ]

    all_files_and_directories['directories'] = sorted(
        [
            {
                'name': d,
                'isEmpty': have_files(os.path.join(final_path, d))
            }
            for d in os.listdir(final_path)
            if os.path.isdir(os.path.join(final_path, d))
        ],
        key=lambda x: x['isEmpty']
    )

    all_files_and_directories['actions'] = [
        {
            'label': 'Create Directory',
            'method': 'POST',
            'url': f"/api/folder/{clean_url}" if url != '/' else "/api/folder/"
        },
        {
            'label': 'Upload File',
            'method': 'POST',
            'url': f"/api/file/{clean_url}" if url != '/' else "/api/file/"
        }
    ]

    if url != '/':
        all_files_and_directories['actions'] += [
            {
                'label': 'Delete',
                'method': 'DELETE',
                'url': f"/api/folder/{clean_url}"
            },
            {
                'label': 'Rename',
                'method': 'PATCH',
                'url': f"/api/folder/{clean_url}"
            }
        ]

    return jsonify({
        'status': 'success',
        'data': all_files_and_directories
    }), 200


@folder_bp.route('/<path:folder_path>', methods=['PATCH'])
@folder_validations
def rename_directory(folder_path: str) -> tuple[Response, int]:

    # Validation handled by decorator
    data = request.get_json()
    new_name = data.get('name')

    base_path = current_app.config['UPLOADED_FILES']
    old_path = os.path.join(base_path, folder_path)
    parent_dir = os.path.dirname(old_path)
    new_path = os.path.join(parent_dir, new_name)

    try:
        os.rename(old_path, new_path)
        return jsonify({'status':'success',
                        'message': 'Directory renamed successfully',
                        'data': {'new_name': new_name}
                        }), 200
    
    except Exception as e:
        return jsonify({'status':'error',
                        'message': f'Error renaming directory: {str(e)}'
                        }), 500
    
@folder_bp.route('/<path:folder_path>', methods=['DELETE'])
@folder_validations
def delete_directory(folder_path: str) -> tuple[Response, int]:

    base_path = current_app.config['UPLOADED_FILES']
    file_path = os.path.join(base_path,folder_path) 

    try:
        shutil.rmtree(file_path, ignore_errors=True)
        return jsonify({'status':'success',
                        'message':'Directory deleted successfully'
                        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error deleting directory: {str(e)}'}), 500

@folder_bp.route('/', methods=['POST'])
@folder_bp.route('/<path:folder_path>', methods=['POST'])
@folder_validations
def create_directory(folder_path: str = '') -> tuple[Response, int]:
    
    base_path = current_app.config['UPLOADED_FILES']    
    final_path = os.path.join(base_path,folder_path)
    
    folder_name = folder_path.split('/')[-1]
    
    try:
        os.makedirs(final_path, exist_ok=True)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({
    'status': 'success',
    'data': {
        'name': folder_name,
        'type': 'directory',
        'size': get_path_size(final_path),
        'path': format_root(folder_path)
    }
    }), 201