from App.modules.serialization_module import serializeList
from .database import db
from datetime import datetime

#Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="orders")
    date_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pickup_status = db.Column(db.String(50), nullable=False)
    products = db.relationship("ProductOrder", back_populates="order",  cascade="all,delete")

    def get_total():
        pass

    def get_invoice():
        pass

    def toDict(self):
        return{
            "id" : self.id,
            "user" : self.user.toDict(),
            "item_count": self.item_count,
            "order_total": round(self.order_total,2),
            "date_placed": self.date_placed.strftime("%a, %d %b, %Y"),
            "status": self.pickup_status,
            # TODO: Test
            "products": serializeList(map(lambda productOrder: productOrder.product, self.products))
        }