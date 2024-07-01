from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/db_konsign?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Custom JWT's Error Messages

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({"message": "Akses gagal. Pastikan anda telah login"}), 466


@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return jsonify({"message": "Token telah expire. Silakan login ulang."}), 466


from app.auth import auth
from app.controllers import (
    product_controller,
    transaction_controller,
    user_controller,
    seller_controller,
    consignment_controller
)
