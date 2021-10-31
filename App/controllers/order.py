from App.models import ( Order )
from App.models.database import db
from App.modules.serialization_module import serializeList

#create order for customer
def create_cust_order(customer, item_count, order_total, status):
    newOrder = Order(user_id = customer.id, item_count = item_count, order_total = order_total, pickup_status = status)
    print("Successfully Created")
    db.session.add(newOrder)
    db.session.commit()
    return newOrder

def add_order_products(Order, OrderProductList):
    db.session.add(Order)
    for OrderProduct in OrderProductList:
        Order.products.append(OrderProduct)
    db.session.commit()

# get list of ALL orders
def get_orders():
    print('get all orders')
    orders = Order.query.all()
    return serializeList(orders)

# get order information - used in invoice part of the app.
def get_order_by_id(order_id):
    print("getting order")
    order = Order.query.filter(Order.id == order_id).first() 
    return order

# get all orders belonging to user - used in profile dashboard to display
# user orders
def get_orders_by_user(email):
    print("getting user's orders")
    orders = Order.query.filter(Order.user.has(email = email)).all()
    return serializeList(orders)

# search through orders - used by admin for - manage orders as 
# this contains a search through ALL orders
def get_orders_by_term(term):
    orders = Order.query.filter(
        Order.id.contains(term)
        | Order.pickup_status.contains(term)
        | Order.user.has(email = term)
        | Order.user.has(first_name = term)
        | Order.user.has(last_name = term)
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