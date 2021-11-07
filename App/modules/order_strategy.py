from App.models.order import Order


class OrderUpdateStrategy():

    def __init__(self, request):
        self.request = request

    def update(self, order: Order):
        order.order_status = self.request.json.get('status')
