# El decorator debe hacer lo siguiente:
#   * Si se va a crear un archivo:
#       * Que realmente haya un archivo adjunto.
#       * Que no traten de hacer nada "raro"
#               Ej: Intentos de XSS en el nombre.
#                               Directory Path Traversal.
#
#   * Si se va a crear una carpeta:
#        * Debo comprobar que no exista antes.
#        * Que no traten de hacer nada "raro"
#               Ej: Intentos de XSS en el nombre.
#                               Directory Path Traversal.
#
#   * Si se va a eliminar uno de los dos se debe comprobar que:
#       * Exista el archivo/carpeta
#       * Que no traten de hacer nada "raro"
#               Ej: Intentos de XSS en el nombre.
#                               Directory Path Traversal.
#

from functools import wraps
from flask import request, jsonify
from app.utils.filesystem import secure_path, get_filetype, have_files

def files_validations(func):
    @wraps(func)
    def wrapper(*args, **kwards):
        pass
    
    return wrapper

def folders_validations(func):
    @wraps(func)
    def wrapper(*args, **kwards):
        pass
    
    return wrapper