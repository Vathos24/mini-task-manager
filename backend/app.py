from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.db import db
from backend.cache import cache
from backend.middleware import register_middleware
from backend.routes import register_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
cache.init_app(app)
JWTManager(app)
CORS(app)

register_middleware(app)
register_routes(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

