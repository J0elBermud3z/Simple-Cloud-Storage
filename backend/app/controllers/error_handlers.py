from flask import jsonify, request, redirect

def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'status': 'error', 'message': 'Not Found'}), 404
        return redirect('/')
    
    @app.errorhandler(500)
    def internal_server_error(e):
        if request.path.startswith('/api/'):
            return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500
        return redirect('/')