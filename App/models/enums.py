from enum import Enum

# Order statuses based on a simple commerce setup
# App frontend handles cart => Products, quantities, current item prices
# App backend handles order status change logic 
# Order stages -> Cart => Confirmed => Picking by staff => Awaiting pickup => Completed & Paid
class OrderStatus(int, Enum):
    CONFIRMED = 1
    PICKING = 2
    AWAITING_PICKUP = 3
    COMPLETED = 4


# These are the roles for the users
# Customer - role=1 can add products, checkout and view orders
# Admins - role =2 Customer + manage products, orders and customers
class UserRole(int, Enum):
    USER = 1,
    ADMIN = 2


# This enum controls the type of payments made by individuals
# 3 categories of payment are maintained currently
# Extending this enum allows tracking of new payment methods when added
class PaymentType(int, Enum):
    CASH = 1,
    LINX = 2,
    CREDIT_CARD = 3