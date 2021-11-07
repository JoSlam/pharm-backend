from enum import Enum

# Enumerable https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
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

class PaymentType(int, Enum):
    CASH = 1,
    LINX = 2,
    CREDIT_CARD = 3