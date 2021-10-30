from App.controllers import (
    create_user,
    get_user,
)
from flask import Blueprint, redirect, render_template, request, abort, jsonify
from flask_jwt import jwt_required, current_identity
import json
from App.models.enums import UserRole


auth_views = Blueprint('auth_views', __name__, template_folder='../templates')



# Login endpoint
@auth_views.route('/login', methods=["POST"]) 
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return 'User not found', 404

        if verifyPassword(user, password):
            access_token = getUserAccessToken(email)
            return {"access_token": access_token}, 200
        else:
            return 'Invalid login credentials', 400
    except AttributeError:
        return 'Invalid message format', 400


# Sign up endpoint
@auth_views.route('/signup', methods=["POST"])
def signup():
    try:
        # get user's data from form
        first_name = request.json.get('fname')
        last_name = request.json.get('lname')
        email = request.json.get('email')
        password = request.json.get('password')
        allergies = request.json.get('allergies')

        # missing arguments
        if not email: 
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400

        # if a user is found, abort
        if get_user(email) is not None:
            return 'User already exists', 403

        print('Creating new user with email {0}'.format(email))
        # create user and jsonify their information for storage
        newUser = create_user(first_name, last_name, email,
                            password, allergies, role=UserRole.USER)

        access_token = getUserAccessToken(email)
        return {"access_token": access_token}, 200
    except AttributeError:
        return 'Missing data', 400


# Authentication test endpoint
@auth_views.route('/user')
@jwt_required()
def get_user_details():
    user = get_jwt_identity()
    return jsonify(user.toDict())