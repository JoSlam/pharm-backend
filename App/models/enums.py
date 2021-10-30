import enum

# Enumerable https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Enum


class OrderStatus(enum.Enum):
    INCART = "In Cart"
    PLACED = "Placed"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"


# These are the roles for the users
# Customer - role=1 can add products, checkout and view orders
# Admins - role =2 Customer + manage products, orders and customers
class UserRole(enum.Enum):
    USER = 1,
    ADMIN = 2
