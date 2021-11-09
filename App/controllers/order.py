from flask import Blueprint, request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from App.controllers.product import get_product_by_slug
from App.controllers.user import get_user_by_email

from App.models import (Order)
from App.database import db
from App.models.enums import OrderStatus
from App.models.productOrder import ProductOrder

from App.modules.serialization_module import serializeList
from App.modules.OrderUpdater.order_updater_factory import GetOrderUpdater, OrderUpdaterFactory


order_bp = Blueprint('order_views', __name__,
                     template_folder='../templates')


# Fetch all orders
@order_bp.route('/orders', methods=["GET"])
@jwt_required()
def display_orders():
    orders = Order.query.all()
    return jsonify(serializeList(orders))


# Get an order by ID
@order_bp.route('/order/<int:order_id>', methods=["GET"])
@jwt_required()
def get_order(order_id):
    try:
        order = get_order_by_id(order_id)
        return jsonify(order.toDict())
    except Exception:
        return f"Unable to fetch order with id: {order_id}", 500


# Create new order
@order_bp.route('/create-order', methods=["POST"])
@jwt_required()
def create_order():
    try:
        identity = get_jwt_identity()
        cart_items = request.json.get('cart')
        newOrder = create_customer_order(identity["email"], OrderStatus.CONFIRMED, cart_items)
        return jsonify(newOrder.toDict())
    except Exception as e:
        print(e)
        return f"Error creating new order", 500
    


@order_bp.route('/progress-order', methods=["POST"])
@jwt_required()
def progress_order():
    try:
        order_id = request.json.get('order_id')
        order_status = request.json.get("order_status")

        order = get_order_by_id(order_id)
        order_updater_factory = OrderUpdaterFactory(request)
        order_updater = order_updater_factory.getUpdater(order_status)

        order_updater.update(order)
        return "Order updated", 200
    except Exception as e:
        print(e)
        return f"Unable to update order {order_id}", 500


# get user orders
@order_bp.route('/user-orders', methods=["GET"])
@jwt_required()
def display_user_orders():
    identity = get_jwt_identity()
    userEmail = identity["email"]

    try:
        orderList = get_orders_by_user(userEmail)
        return jsonify(orderList)
    except Exception:
        return f"Unable to fetch orders for user: {userEmail}", 500

# create new customer order
def create_customer_order(user_email, order_status, cart_items):
    user = get_user_by_email(user_email)
    new_order = Order(user_id=user.id, order_status=order_status)

    # Add order object to DB
    db.session.add(new_order)
    db.session.commit()
    print(f"Created new order for user: {user_email}")

    product_orders = create_product_orders(new_order, cart_items)

    # Add product orders to the order
    add_products_to_order(new_order, product_orders)
    return new_order


def add_products_to_order(order, productOrders):
    order.products.extend(productOrders)
    db.session.add(order)
    db.session.commit()


def create_product_orders(new_order, cart_items):
    # Create product orders
    product_orders = []
    for item in cart_items:
        product = get_product_by_slug(item["product_slug"])
        
        if product is not None:
            price = item["current_price"]
            quantity = item["quantity"]

            product.QoH -= quantity

            new_product_order = ProductOrder(order_id=new_order.id, product_id=product.id, quantity=quantity, current_price=price)
            print(f"Created product order for: {product.product_name} order: {new_order.id}")
            product_orders.append(new_product_order)

    # Commit all product orders to the DB
    db.session.add_all(product_orders)
    db.session.commit()
    return product_orders



# get order information by its id
def get_order_by_id(order_id):
    return Order.query.filter_by(id=order_id).first()


# get all orders belonging to user - used in profile dashboard to display
# user orders
def get_orders_by_user(email):
    print("getting user's orders")
    orders = Order.query.filter(Order.user.has(email=email)).all()
    return serializeList(orders)


# search through orders - used by admin for - manage orders as
# this contains a search through ALL orders
def get_orders_by_term(term):
    orders = Order.query.filter(
        Order.id.contains(term)
        | Order.user.has(email=term)
        | Order.user.has(first_name=term)
        | Order.user.has(last_name=term)
        | Order.order_total.contains(term)
        | Order.date_placed.contains(term)
    )
    return serializeList(orders)
