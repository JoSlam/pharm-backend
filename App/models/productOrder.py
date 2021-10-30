from .database import db
from App.models.enums import OrderStatus
# a product can be in multiple orders and an order can contain multiple
#products - MANY TO MANY relationship - Association Model
# Reference - https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object 
class ProductOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="orders")
    order = db.relationship("Order", back_populates="products")
    quantity = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Enum(OrderStatus))
    #prices may change, this is the price of the product at the time of order confirmation
    current_price = db.Column(db.Float, nullable = False)