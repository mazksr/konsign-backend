from app import db

class Seller(db.Model):
    __tablename__ = "seller"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    seller_balance = db.Column(db.Integer, nullable=False)
    bank = db.Column(db.String(100))
    bank_number = db.Column(db.String(100))
    ewallet_number = db.Column(db.String(100))

    user = db.relationship("User", back_populates="seller")
    consignments = db.relationship("Consignment", back_populates="seller")

    def __init__(self, id, user_id, seller_balance, bank, bank_number, ewallet_number):
        self.id = id
        self.user_id = user_id
        self.seller_balance = seller_balance
        self.bank = bank
        self.bank_number = bank_number
        self.ewallet_number = ewallet_number