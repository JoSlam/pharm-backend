from App.models import User
from App.models.database import db
from App.modules.auth_module import setUserPassword
from App.modules.serialization_module import serializeList

# create USER
def create_user(firstname, lastname, email, password, allergy, role):
    newUser = User(first_name=firstname, last_name=lastname,
                   email=email, allergies=allergy, role=role)
    setUserPassword(newUser, password)
    db.session.add(newUser)
    db.session.commit()
    print("User successfully created")
    return newUser

# get user by email
def get_user_by_email(email):
    print("Fetching user with email {0}".format(email))
    user = User.query.filter_by(email=email).first()
    return user

# get all users - used by admin in - manage users
def get_users():
    print('get_users')
    users = User.query.all()
    serializeList(users)
