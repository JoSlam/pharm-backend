from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

customer_views = Blueprint('customer_views', __name__, template_folder='../templates')

from App.controllers import (
    get_customers,
    delete_customer_by_email,
)

# get list of all customers and return it to frontend
@customer_views.route('/customers', methods=["GET"])
@jwt_required()
def display_customers():
    customerList = get_customers()
    return jsonify(customerList)

#Deletes customer from database and returns if it was successful
@customer_views.route('/delete-customer', methods=["DELETE"])
def delete_customer():
    customer_email = request.args.get("email")
    deleted = delete_customer_by_email(customer_email)
    return jsonify({"deleted" : deleted})

