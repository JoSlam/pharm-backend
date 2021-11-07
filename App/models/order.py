from re import match
from .database import db
from functools import reduce

from App.models.enums import OrderStatus, PickupStatus
from App.modules.serialization_module import serializeList


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="orders")
    date_placed = db.Column(db.DateTime)
    order_status = db.Column(db.Enum(OrderStatus), default=OrderStatus.INCART)
    pickup_status = db.Column(db.Enum(PickupStatus),
                              default=PickupStatus.NOT_READY)
    products = db.relationship(
        "ProductOrder", back_populates="order",  cascade="all,delete")

    @property
    def order_total(self):
        return reduce(lambda x, y: x.currentPrice + y.currentPrice, self.products, 0)

    @property
    def item_count(self):
        return len(self.products)

    def get_invoice():
        pass


    # TODO: move to somewhere else
    # def notify(self, status: OrderStatus):
    #     #current order status
    #     if self.order_status == OrderStatus.INCART:
    #         if status == OrderStatus.CONFIRMED:
    #             # Iterate product orders
    #             # Decrement all product quantities by product order quantity
    #             for item in self.products:
    #                 item.product.QoH -= item.quantity
    #             db.session.add_all(self.products)
    #             db.session.commit()       




    def toDict(self):
        return{
            "id": self.id,
            "user": self.user.toDict(),
            "item_count": self.item_count,
            "order_total": round(self.order_total, 2),
            "date_placed": self.date_placed.strftime("%a, %d %b, %Y"),
            "order_status": self.order_status,
            "pickup_status": self.pickup_status,
            # TODO: Test
            "products": serializeList(map(lambda productOrder: productOrder.product, self.products))
        }
