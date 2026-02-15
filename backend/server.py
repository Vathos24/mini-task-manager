from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Serve static HTML files
app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    if os.path.exists(path) and path.endswith('.html'):
        return send_from_directory('.', path)
    return "File not found", 404

if __name__ == '__main__':
    print("Serving frontend at http://localhost:3000")
    app.run(port=3000, debug=True)