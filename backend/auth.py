from flask_jwt_extended import create_access_token

def login(username, password):
    # hardcoded user for now
    if username == "admin" and password == "password":
        return create_access_token(identity=username)
    return None

