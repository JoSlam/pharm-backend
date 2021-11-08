from datetime import datetime
from App.database import db
from App.models.payment import Payment
from .order_updater import OrderUpdater


class CompletedOrderUpdater(OrderUpdater):
    def update(self, order):
        super().update(order)
        
        completed_date = datetime.now()
        order.date_completed = completed_date

        amount = self.request.json.get('amount')
        payment_type = self.request.json.get('payment_type')
        payment = Payment(order_id=order.id, date_created=completed_date, payment_type=payment_type, amount=amount)

        db.session.add(order)
        db.session.commit()

        db.session.add(payment)
        db.session.commit()