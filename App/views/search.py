from flask import request,jsonify, Blueprint
import json
from flask_jwt_extended import jwt_required

search_view = Blueprint('search_view', __name__, template_folder='../templates')


from App.controllers import (
    get_products_by_term,
    get_orders_by_term,
    get_customers_by_term,
)

#endpoint for searching products
@search_view.route('/search-product', methods=["POST"])
def search_product():
    term = request.json.get('term')
    products = get_products_by_term(term)
    return jsonify(products)

#endpoint for searching orders
@search_view.route('/search-order', methods=["POST"])
@jwt_required()
def search_order():
    term = request.json.get('term')
    orders = get_orders_by_term(term)
    return jsonify(orders)

#endpoint for searching customers
@search_view.route('/search-customer', methods=["POST"])
@jwt_required()
def search_customer():
    term = request.json.get('term')
    customers = get_customers_by_term(term)
    return jsonify(customers)
