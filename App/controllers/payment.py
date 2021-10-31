from App.models import Payment
from App.models.database import db

def create_payment(status, amount, date_paid):
    newPayment = Payment(status = status, amount_paid = amount, date_paid = date_paid)
    db.session.add(newPayment)
    db.session.commit()
    return newPayment

