from app import db
from sqlalchemy import Enum

class Consignment(db.Model):
    __tablename__ = "consignment"
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"), nullable=False)

    product = db.relationship("Product", back_populates="consignment")
    seller = db.relationship("Seller", back_populates="consignments")
    transaction = db.relationship("Transaction", back_populates="consignment", uselist=False)

    def __init__(self, id, product, seller):
        self.id = id
        self.product = product
        self.seller = seller