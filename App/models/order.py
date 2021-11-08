from App.database import db
from functools import reduce
from datetime import datetime

from App.models.enums import OrderStatus
from App.modules.serialization_module import serializeList


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="orders")
    date_placed = db.Column(db.DateTime, default=datetime.now)
    date_completed = db.Column(db.DateTime)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.CONFIRMED)
    products = db.relationship(
        "ProductOrder", back_populates="order",  cascade="all,delete")

    @property
    def order_total(self):
        return reduce(lambda x, y: x + y.current_price * y.quantity, self.products, 0.0)

    @property
    def item_count(self):
        return reduce(lambda x, y: x + y.quantity, self.products, 0)

    def get_invoice():
        pass



    def toDict(self):
        return{
            "id": self.id,
            "user": self.user.toDict(),
            "item_count": self.item_count,
            "order_total": round(self.order_total, 2),
            "date_placed": self.date_placed.strftime("%a, %d %b, %Y"),
            "date_completed": self.date_completed,
            "order_status": self.order_status,
            "products": serializeList(list(map(lambda productOrder: productOrder.product, self.products)))
        }
