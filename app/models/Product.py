from app import db
from sqlalchemy import Enum

class Product(db.Model):
    __tablename__ = "product"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    condition = db.Column(Enum("baru", "bekas", name="product_condition"), nullable=False)

    consignment = db.relationship("Consignment", back_populates="product", uselist=False)

    def __init__(self, id, name, image_url, description, price, stock, condition):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.description = description
        self.price = price
        self.stock = stock
        self.condition = condition
