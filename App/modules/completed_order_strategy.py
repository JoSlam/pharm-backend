from App.models.database import db
from datetime import datetime
from App.models.payment import Payment
from App.modules import order_update_strategy


class CompletedOrderStrategy(order_update_strategy):
    def update(self, order):
        super().update(order)
        
        completed_date = datetime.now
        order.date_completed = completed_date

        amount = self.request.json.get('amount')
        payment = Payment(order_id=order.id, timestamp=completed_date, type=type, amount=amount)

        db.session.add(payment)
        db.session.commit()