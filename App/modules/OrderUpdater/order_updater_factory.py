from App.models.enums import OrderStatus
from .order_updater import OrderUpdater
from .completed_order_updater import CompletedOrderUpdater

def GetOrderUpdater(order_status: OrderStatus, request):
    if order_status == OrderStatus.COMPLETED:
        return CompletedOrderUpdater(order_status, request)
    else:
        return OrderUpdater(order_status, request)
        
