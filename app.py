from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
from cache import cache
from middleware import register_middleware
from routes import register_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
cache.init_app(app)
JWTManager(app)

register_middleware(app)
register_routes(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

