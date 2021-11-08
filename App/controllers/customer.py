from App.models import (User)
from App.database import db
from App.models.enums import UserRole
from App.modules.serialization_module import serializeList

# gets customers by filtering users based on their roles
def get_customers():
    print('Fetching all customers')
    customers = User.query.filter_by(role=UserRole.USER)
    return serializeList(customers)
    

# This is used for searching through customers by their attributes in
# admin - manage customers on the frontend
def get_customers_by_term(term):
    customers = User.query.filter(
        (User.role.contains(UserRole.ADMIN)) &
        (User.allergies.contains(term)
         | User.email.contains(term)
         | User.first_name.contains(term)
         | User.last_name.contains(term))
    )
    return serializeList(customers)


# method for deleting customer at /delete-customer endpoint
def delete_customer_by_email(email):
    print("deleting customer")
    customer = User.query.filter(User.email == email).first()
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return True
    return False
