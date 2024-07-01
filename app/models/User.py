from app import db

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))

    seller = db.relationship("Seller", back_populates="user", uselist=False)
    transactions = db.relationship("Transaction", back_populates="buyer")

    def __init__(self, is_admin, id, username, password, email, name, address, phone_number):
        self.id = id
        self.is_admin = is_admin
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.address = address
        self.phone_number = phone_number