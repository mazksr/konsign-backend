import sqlalchemy.exc
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, db
from flask import request, jsonify

from app.models.Seller import Seller
from app.models.User import User

@app.route("/user", methods=["POST"])
def create_user():
    if request.method == "POST":
        id = None
        if "is_admin" in request.json:
            is_admin = request.json["is_admin"]
        else:
            is_admin = False
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]
        name = request.json["name"] if "name" in request.json else None
        address = request.json["address"] if "address" in request.json else None
        phone_number = request.json["phone_number"] if "phone_number" in request.json else None

        new_user = User(id=id, is_admin=is_admin, username=username, email=email, password=password, name=name, address=address, phone_number=phone_number)

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User added successfully"})
        except sqlalchemy.exc.IntegrityError as e:
            if "email" in str(e.orig):
                return jsonify({"message": "Email already exists"}), 466
            elif "username" in str(e.orig):
                return jsonify({"message": "Username already exists"}), 466


@app.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    search = request.args.get("search") if request.args.get("search") else ""
    if request.method == "GET":
        users = User.query.all()
        users_list = []
        for user in users:
            if search.lower() not in user.username.lower() or user.is_admin:
                continue
            seller = Seller.query.filter_by(user_id=user.id).first()
            users_list.append({
                "id": user.id,
                "is_admin": user.is_admin,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "address": user.address,
                "phone_number": user.phone_number,
                "seller_balance": seller.seller_balance if seller else "None"
            })
        return jsonify(users_list)


@app.route("/user/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def user_id(id):
    user = User.query.get_or_404(id)
    if request.method == "GET":
        return jsonify(
            {
                "id": user.id,
                "is_admin": user.is_admin,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "address": user.address,
                "phone_number": user.phone_number
            }
        )

    if request.method == "PUT":
        user.is_admin = request.json["is_admin"] if "is_admin" in request.json else False
        user.username = request.json["username"]
        user.password = request.json["password"]
        user.email = request.json["email"]
        user.name = request.json["name"]
        user.address = request.json["address"]
        user.phone_number = request.json["phone_number"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"})

    if request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})

@app.route("/user/current", methods=["GET", "PUT"])
@jwt_required()
def usr():
    current_id = get_jwt_identity()
    user = User.query.get_or_404(current_id)
    if request.method == "GET":
        seller = Seller.query.filter_by(user_id=current_id).first()
        return jsonify(
            {
                "id": user.id,
                "is_admin": user.is_admin,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "address": user.address,
                "phone_number": user.phone_number,
                "is_seller": seller is not None
            }
        )
    if request.method == "PUT":
        user.username = request.json["username"]
        if "password" in request.json and request.json["password"]:
            user.password = request.json["password"]
        user.email = request.json["email"]
        user.name = request.json["name"]
        user.address = request.json["address"]
        user.phone_number = request.json["phone_number"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
