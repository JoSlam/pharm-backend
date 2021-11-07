from App.models.enums import OrderStatus
from App.modules import completed_order_strategy, order_update_strategy

def GetOrderUpdater(order_status: OrderStatus, request):
    if order_status == OrderStatus.COMPLETED:
        return completed_order_strategy(request)
    else:
        return order_update_strategy(request)
        
