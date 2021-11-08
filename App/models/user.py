from App.database import db
from App.models.enums import UserRole
from App.modules.auth_module import getPasswordHash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    allergies = db.Column(db.String(300))
    passwordHash = db.Column(db.String(120))
    role = db.Column(db.Enum(UserRole))
    DOB = db.Column(db.DateTime, nullable=True)
    orders = db.relationship(
        "Order",  back_populates="user", cascade="all,delete")

    def setPassword(self, password):
        self.password = getPasswordHash(password)

    def toDict(self):
        return{
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role,
            'allergies': self.allergies
        }
