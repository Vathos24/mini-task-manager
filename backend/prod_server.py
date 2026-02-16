import os
from waitress import serve
from backend.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    host = os.environ.get("HOST", "0.0.0.0")
    serve(app, host=host, port=port)
