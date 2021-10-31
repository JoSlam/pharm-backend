from enum import Enum

# Enumerable https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum
class OrderStatus(int, Enum):
    INCART = 1
    PLACED = 2
    CONFIRMED = 3
    COMPLETED = 4

class PickupStatus(int, Enum):
    NOT_READY = 1
    READY = 2
    COMPLETED = 3


# These are the roles for the users
# Customer - role=1 can add products, checkout and view orders
# Admins - role =2 Customer + manage products, orders and customers
class UserRole(int, Enum):
    USER = 1,
    ADMIN = 2
