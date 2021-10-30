# from App.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# This module contains the loging for all authentication operations in the app

def getUserAccessToken(email):
    return create_access_token(identity={"email": email})

def setUserPassword(user, password):
    user.passwordHash = getPasswordHash(password)


def authenticateUser(email, password):
    user = User.query.filter_by(email=email).first()
    if user and verifyPassword(email, password):
        return user


def identityHandler(payload):
    return User.query.filter_by(id=payload['identity']).first()


def verifyPassword(user, password):
    return check_password_hash(user.passwordHash, password)


def getPasswordHash(password):
    return generate_password_hash(password, method="sha256")
