from App.database import db
from datetime import datetime
from App.models.enums import PaymentType


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', backref='payment')
    payment_type = db.Column(db.Enum(PaymentType), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def toDict(self):
        return {
            "id": self.id,
            "order": self.order.toDict(),
            "type": self.payment_type,
            "amount": self.amount,
            "date_created": self.date_created
        }
