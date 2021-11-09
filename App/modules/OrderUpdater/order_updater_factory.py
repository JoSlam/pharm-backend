from App.models.enums import OrderStatus
from .order_updater import OrderUpdater
from .completed_order_updater import CompletedOrderUpdater

class OrderUpdaterFactory():
    
    def __init__(self, request):
        self.request = request

    def getUpdater(self, order_status: OrderStatus):
        if order_status == OrderStatus.COMPLETED:
            return CompletedOrderUpdater(order_status, self.request)
        else:
            return OrderUpdater(order_status, self.request)
        
