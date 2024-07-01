from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from flask import request, jsonify
from app.models.Transaction import Transaction
from app.models.Consignment import Consignment
from app.models.Product import Product
from app.models.Seller import Seller
from app.models.Consignment import Consignment

@app.route("/transaction", methods=["POST", "GET"])
@jwt_required()
def manage_transactions():
    search = request.args.get("search") if request.args.get("search") else ""
    if request.method == "POST":
        data = request.json
        user_id = get_jwt_identity()
        new_transaction = Transaction(
            id=None,
            consignment_id=data["consignment_id"],
            amount=data["amount"],
            buyer_id=user_id,
            total_price=data["total_price"],
            buyer_notes=data["buyer_notes"],
            tracking_number="",
            payment=data["payment"],
            order_status="waiting payment",
        )
        consignment = Consignment.query.get(data["consignment_id"])
        product = Product.query.get(consignment.product_id)
        product.stock -= data["amount"]
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({"message": "Transaction added successfully"})

    if request.method == "GET":
        transactions = Transaction.query.all()
        transactions_list = []
        for transaction in transactions:
            consignment = Consignment.query.get(transaction.consignment_id)
            product = Product.query.get(consignment.product_id)
            if search.lower() not in product.name.lower():
                continue
            transaction_data = {
                "id": transaction.id,
                "item_name": product.name,
                "total_price": transaction.total_price,
                "amount": transaction.amount,
                "order_status": transaction.order_status,
                "tracking_number": transaction.tracking_number,
                "payment": transaction.payment,
                "buyer_notes": transaction.buyer_notes,
            }
            transactions_list.append(transaction_data)
        return jsonify(transactions_list)


@app.route("/transaction/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
            "id": transaction.id,
            "consignment_id": transaction.consignment_id,
            "amount": transaction.amount,
            "buyer_id": transaction.buyer_id,
            "total_price": transaction.total_price,
            "buyer_notes": transaction.buyer_notes,
            "tracking_number": transaction.tracking_number,
            "payment": transaction.payment,
            "order_status": transaction.order_status,

        })

    if request.method == "PUT":
        data = request.json
        transaction.consignment_id = data["consignment_id"]
        transaction.amount = data["amount"]
        transaction.buyer_id = data["buyer_id"]
        transaction.total_price = data["total_price"]
        transaction.buyer_notes = data["buyer_notes"]
        transaction.tracking_number = data["tracking_number"]
        transaction.payment = data["payment"]
        transaction.order_status = data["order_status"]
        db.session.commit()
        return jsonify({"message": "Transaction updated successfully"})

    if request.method == "DELETE":
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction deleted successfully"})

@app.route("/transaction/confirm/<id>", methods=["PUT"])
@jwt_required()
def confirm(id):
    status = ["waiting payment", "seller notified", "processed", "shipping", "completed"]
    transaction = Transaction.query.get_or_404(id)
    if request.method == "PUT":
        if transaction.order_status == "processed":
            transaction.tracking_number = request.json["tracking_number"]
            transaction.order_status = "shipping"
            db.session.commit()
            return jsonify({"message": "Tracking Number Updated"}), 200
        if status.index(transaction.order_status) < 3:
            transaction.order_status = status[status.index(transaction.order_status) + 1]
        else:
            consignment = Consignment.query.get(transaction.consignment_id)
            print(consignment)
            seller = Seller.query.get(consignment.seller_id)
            print(seller)
            seller.seller_balance += transaction.total_price
            transaction.order_status = "completed"
        db.session.commit()
        return jsonify({"message": "Transaction updated successfully"})

@app.route("/transaction/cancel/<id>", methods=["PUT"])
@jwt_required()
def cancel(id):
    transaction = Transaction.query.get_or_404(id)
    consignment = Consignment.query.get(transaction.consignment_id)
    product = Product.query.get(consignment.product_id)
    if request.method == "PUT":
        transaction.order_status = "canceled"
        product.stock += transaction.amount
        db.session.commit()
        return jsonify({"message": "Transaction cancelled successfully"})


@app.route("/transaction/current", methods=["POST", "GET", "PUT", "DELETE"])
@jwt_required()
def trnsc():
    current_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(buyer_id=current_id).all()
    search = request.args.get("search") if request.args.get("search") else ""
    if request.method == "GET":
        transactions_list = []
        for transaction in transactions:
            consignment = Consignment.query.get(transaction.consignment_id)
            product = Product.query.get(consignment.product_id)
            if search.lower() not in product.name.lower():
                continue
            transaction_data = {
                "id": transaction.id,
                "item_name": product.name,
                "total_price": transaction.total_price,
                "amount": transaction.amount,
                "order_status": transaction.order_status,
                "tracking_number": transaction.tracking_number,
            }
            transactions_list.append(transaction_data)
        return jsonify(transactions_list)

@app.route("/orders", methods=["POST", "GET", "PUT", "DELETE"])
@jwt_required()
def orders():
    search = request.args.get("search") if request.args.get("search") else ""
    if request.method == "GET":
        current_id = get_jwt_identity()
        seller = Seller.query.filter_by(user_id=current_id).first()
        consignments = Consignment.query.filter_by(seller_id=seller.id).all()
        if not seller:
            return jsonify([]), 404
        transactions_list = []
        for consignment in consignments:
            product = Product.query.get(consignment.product_id)
            if search.lower() not in product.name.lower():
                continue
            transactions = Transaction.query.filter_by(consignment_id=consignment.id).order_by(Transaction.id.asc()).all()
            for transaction in transactions:
                transaction_data = {
                    "id": transaction.id,
                    "item_name": product.name,
                    "total_price": transaction.total_price,
                    "amount": transaction.amount,
                    "order_status": transaction.order_status,
                    "buyer_notes": transaction.buyer_notes,
                }
                transactions_list.append(transaction_data)

        return jsonify(transactions_list)

