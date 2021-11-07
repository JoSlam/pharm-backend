from .database import db
from datetime import datetime
from App.models.enums import PaymentType


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'order.id'), primary_key=True)
    order = db.relationship('Order', backref='payment', lazy=True)
    type = db.Column(db.Enum(PaymentType), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    def toDict(self):
        return {
            "id": self.id,
            "order": self.order.toDict(),
            "type": self.type,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
