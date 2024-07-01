from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, db
from flask import request, jsonify
from app.models.Seller import Seller
from app.models.User import User

@app.route("/seller", methods=["POST", "GET"])
@jwt_required()
def manage_sellers():
    if request.method == "POST":
        data = request.json
        new_seller = Seller(
            id=None,
            user_id=data["user_id"],
            seller_balance=data["seller_balance"],
            bank=data["bank"],
            bank_number=data["bank_number"],
            ewallet_number=data["ewallet_number"]
        )
        db.session.add(new_seller)
        db.session.commit()
        return jsonify({"message": "Seller added successfully"})

    if request.method == "GET":
        sellers = Seller.query.all()
        sellers_list = [{
            "id": seller.id,
            "user_id": seller.user_id,
            "seller_balance": seller.seller_balance,
            "bank": seller.bank,
            "bank_number": seller.bank_number,
            "ewallet_number": seller.ewallet_number
        } for seller in sellers]
        return jsonify(sellers_list)


@app.route("/seller/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_seller(id):
    seller = Seller.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
            "id": seller.id,
            "user_id": seller.user_id,
            "seller_balance": seller.seller_balance,
            "bank": seller.bank,
            "bank_number": seller.bank_number,
            "ewallet_number": seller.ewallet_number
        })
    
    if request.method == "PUT":
        data = request.json
        seller.seller_balance = data["seller_balance"]
        seller.bank = data["bank"]
        seller.bank_number = data["bank_number"]
        seller.ewallet_number = data["ewallet_number"]
        db.session.commit()
        return jsonify({"message": "Seller updated successfully"})
    
    if request.method == "DELETE":
        db.session.delete(seller)
        db.session.commit()
        return jsonify({"message": "Seller deleted successfully"})

@app.route("/seller/current", methods=["GET", "PUT"])
@jwt_required()
def seller_self():
    current_id = get_jwt_identity()
    user = User.query.get_or_404(current_id)
    seller = Seller.query.filter_by(user_id=user.id).first()
    if not seller:
        return jsonify({"message": "Seller not found"}), 404

    if request.method == "GET":
        return jsonify({
            "id": seller.id,
            "user_id": seller.user_id,
            "seller_balance": seller.seller_balance,
            "bank": seller.bank,
            "bank_number": seller.bank_number,
            "ewallet_number": seller.ewallet_number
        })

    if request.method == "PUT":
        data = request.json
        seller.bank = data["bank"]
        seller.bank_number = data["bank_number"]
        seller.ewallet_number = data["ewallet_number"]
        db.session.commit()
        return jsonify({"message": "Seller updated successfully"})