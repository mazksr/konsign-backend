from datetime import datetime

from flask_jwt_extended import jwt_required

from app import app, db
from flask import request, jsonify
from app.models.Consignment import Consignment

@app.route("/consignment", methods=["POST", "GET"])
@jwt_required()
def manage_consignments():
    if request.method == "POST":
        data = request.json
        new_consignment = Consignment(
            id=None,
            product_id=data["product_id"],
            seller_id=data["seller_id"],
        )
        db.session.add(new_consignment)
        db.session.commit()
        return jsonify({"message": "Consignment added successfully"})

    if request.method == "GET":
        consignments = Consignment.query.all()
        consignments_list = [{
            "id": consignment.id,
            "product_id": consignment.product_id,
            "seller_id": consignment.seller_id,
        } for consignment in consignments]
        return jsonify(consignments_list)


@app.route("/consignment/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_consignment(id):
    consignment = Consignment.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
            "id": consignment.id,
            "product_id": consignment.product_id,
            "seller_id": consignment.seller_id,
        })

    if request.method == "PUT":
        data = request.json
        consignment.product_id = data["product_id"]
        consignment.seller_id = data["seller_id"]
        db.session.commit()
        return jsonify({"message": "Consignment updated successfully"})

    if request.method == "DELETE":
        db.session.delete(consignment)
        db.session.commit()
        return jsonify({"message": "Consignment deleted successfully"})
