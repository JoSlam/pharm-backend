from App.database import db

class OrderUpdater():

    def __init__(self, order_status, request):
        self.request = request
        self.order_status = order_status

    def update(self, order):
        order.order_status = self.order_status

        db.session.add(order)
        db.session.commit()
