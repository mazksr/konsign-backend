from sqlalchemy import Enum
from app import db

class Transaction(db.Model):
    __tablename__ = "transaction"
    
    id = db.Column(db.Integer, primary_key=True)
    consignment_id = db.Column(db.Integer, db.ForeignKey("consignment.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    buyer_notes = db.Column(db.String(200))
    tracking_number = db.Column(db.String(100))
    payment = db.Column(Enum("BNI", "BRI", "e-wallet", name="payment_method"), nullable=False)
    order_status = db.Column(Enum("waiting payment", "seller notified", "processed", "shipping", "completed", "canceled", name="order_status"), nullable=False)

    consignment = db.relationship("Consignment", back_populates="transaction")
    buyer = db.relationship("User", back_populates="transactions")

    def __init__(self, id, consignment_id, amount, buyer_id, total_price, buyer_notes, tracking_number, payment, order_status):
        self.id = id
        self.consignment_id = consignment_id
        self.amount = amount
        self.buyer_id = buyer_id
        self.total_price = total_price
        self.buyer_notes = buyer_notes
        self.tracking_number = tracking_number
        self.payment = payment
        self.order_status = order_status
