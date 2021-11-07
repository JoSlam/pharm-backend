from flask import Blueprint, request, jsonify
from App.modules.order_updater_factory import GetOrderUpdater
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from App.controllers.product import get_product_by_slug
from App.controllers.productOrder import create_order_product
from App.controllers.user import get_user_by_email

from App.models import (Order)
from App.models.database import db
from App.models.enums import OrderStatus
from App.models.productOrder import ProductOrder
from App.modules.serialization_module import serializeList

order_bp = Blueprint('order_views', __name__,
                     template_folder='../templates')


@order_bp.route('/progress-order/<int: order_id>', methods=["POST"])
@jwt_required
def progress_order(order_id):
    try:
        # TODO: Test
        order = get_order_by_id(order_id)
        order_status = request.json.get("order_status")
        order_updater = GetOrderUpdater(order_status, request)

        order_updater.update(order)
        return "Order updated", 200
    except Exception:
        return f"Unable to update order {order_id}", 500


# get all orders
@order_bp.route('/orders', methods=["GET"])
@jwt_required()
def display_orders():
    orderList = get_orders()
    return jsonify(orderList)


# get user orders
@order_bp.route('/user-orders', methods=["GET"])
@jwt_required()
def display_user_orders():
    identity = get_jwt_identity()
    userEmail = identity["email"]
    orderList = get_orders_by_user(userEmail)
    return jsonify(orderList)


# create order
@order_bp.route('/create-order', methods=["POST"])
@jwt_required()
def create_order():
    identity = get_jwt_identity()
    cart_items = request.json.get('cart')

    newOrder = create_customer_order(identity["email"], OrderStatus.CONFIRMED, cart_items)

    return jsonify(newOrder.toDict())


# get specific order by ID
@order_bp.route('/order', methods=["GET"])
def get_order():
    order_id = request.args.get("id")
    order = get_order_by_id(order_id)
    return jsonify(order.toDict())



# create new customer order
def create_customer_order(user_email, order_status, pickup_status, cart_items):
    user = get_user_by_email(user_email)
    new_order = Order(user_id=user.id, order_status=order_status,
                      pickup_status=pickup_status)

    # Add order object to DB
    db.session.add(new_order)
    db.session.commit()
    print(f"Created new order for user: {user_email}")

    product_orders = create_product_orders(new_order, cart_items)

    # Add product orders to the order
    add_products_to_order(new_order, product_orders)
    return new_order


def create_product_orders(new_order, cart_items):
    # Create product orders
    product_orders = []
    for item in cart_items:
        product = get_product_by_slug(item["product_slug"])
        price = item["current_price"]
        quantity = item["quantity"]

        new_product_order = ProductOrder(
            order_id=new_order.id, product_id=product.id, quantity=quantity, current_price=price)
        print(
            f"Created product order for: {product.product_name} order: {new_order.id}")
        db.session.add(new_product_order)
        product_orders.append(new_product_order)

    # Commit all product orders to the DB
    db.session.commit()
    return product_orders


def add_products_to_order(order, productOrders):
    for productOrder in productOrders:
        order.products.append(productOrder)
    db.session.add(order)


# get list of ALL orders
def get_orders():
    print('get all orders')
    orders = Order.query.all()
    return serializeList(orders)


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
        | Order.pickup_status.contains(term)
        | Order.user.has(email=term)
        | Order.user.has(first_name=term)
        | Order.user.has(last_name=term)
        | Order.order_total.contains(term)
        | Order.date_placed.contains(term)
    )
    return serializeList(orders)


# Used by admin to update order status
def update_order_by_id(order_id, status):
    print("updating order")
    order = Order.query.filter(Order.id == order_id).first()
    order.pickup_status = status
    db.session.add(order)
    db.session.commit()
    return order
