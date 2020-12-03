from flask import Blueprint, redirect, render_template, request, jsonify
from flask_jwt import jwt_required, current_identity
import json

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

from App.controllers import (
    get_users,
    authenticate
)

@auth_views.route('/auth', methods=["POST"])
def auth():
    uwi_id = request.form["uwi_id"]
    password = request.form["password"]
    token = authenticate(uwi_id, password)
    return json.dumps(token)

@auth_views.route('/test')
@jwt_required()
def protected():
    return json.dumps(current_identity.username)

