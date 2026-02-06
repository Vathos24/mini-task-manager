from flask import request, jsonify

def register_middleware(app):

    @app.before_request
    def before():
        if request.method == "POST" and not request.is_json:
            return jsonify(error="JSON only"), 415

