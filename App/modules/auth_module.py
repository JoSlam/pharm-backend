# from App.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

# from App.models import User

# This module contains the logic for all authentication operations in the app


def getUserAccessToken(email):
    return create_access_token(identity={"email": email})


def setUserPassword(user, password):
    user.passwordHash = getPasswordHash(password)


def verifyPassword(user, password):
    return check_password_hash(user.passwordHash, password)


def getPasswordHash(password):
    return generate_password_hash(password, method="sha256")
