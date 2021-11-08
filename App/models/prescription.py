#Not in use yet as no perscription order upload feature is available for project scope
from datetime import datetime
from App.database import db
from .order import Order

class Prescription(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def createPrescriptionOrder():
        return ""

    def toDict(self):
        return ""

