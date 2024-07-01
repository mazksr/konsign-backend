from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, db
from flask import request, jsonify

from app.models.Consignment import Consignment
from app.models.Product import Product
from app.models.Seller import Seller
from app.models.Transaction import Transaction
from app.models.User import User

@app.route("/product", methods=["GET"])
@jwt_required(optional=True)
def get_products():
    search = request.args.get("search") if request.args.get("search") else ""
    own_products = []
    user_id = get_jwt_identity()
    if user_id:
        seller = Seller.query.filter_by(user_id=user_id).first()
        if seller:
            consignments = Consignment.query.filter_by(seller_id=seller.id).all()
            own_products = [consignment.product_id for consignment in consignments]
    if request.method == "GET":
        products = Product.query.order_by(Product.id.desc()).all()
        products_list = []
        for product in products:
            if search.lower() not in product.name.lower() or product.stock == -1:
                continue
            product = {
                "id": product.id,
                "name": product.name,
                "image_url": product.image_url,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "condition": product.condition,
                "consignment_id": (Consignment.query.filter_by(product_id=product.id).first()).id,
                "own_product": True if own_products and product.id in own_products else False
            }
            products_list.append(product)
        return jsonify(products_list)

@app.route("/product", methods=["POST"])
@jwt_required()
def manage_products():
    if request.method == "POST":
        data = request.json
        new_product = Product(
            id=None,
            name=data["name"],
            image_url=data["image_url"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"],
            condition=data["condition"]
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})


@app.route("/product/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_product(id):
    product = Product.query.get_or_404(id)

    if request.method == "GET":
        if product.stock == -1:
            return jsonify({"message": "Product not found"}), 404
        return jsonify({
            "id": product.id,
            "name": product.name,
            "image_url": product.image_url,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "condition": product.condition
        })

    if request.method == "PUT":
        data = request.json
        product.name=data["name"]
        if "image_url" in data and data["image_url"]:
            product.image_url = data["image_url"]
        product.description=data["description"]
        product.price=data["price"]
        product.stock=data["stock"]
        product.condition=data["condition"]
        db.session.commit()
        return jsonify({"message": "Product updated successfully"})

    if request.method == "DELETE":
        consignment = Consignment.query.filter_by(product_id=id).first()
        transaction = Transaction.query.filter_by(consignment_id=consignment.id).first()
        if transaction and (transaction.order_status not in ("canceled", "completed")):
            print(transaction.order_status, transaction.id)
            return jsonify({"message": "Product cannot be deleted because it is in an ongoing transaction"}), 400
        product.name = "Product deleted"
        product.stock = -1
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})

@app.route("/product/current", methods=["POST", "GET", "PUT"])
@jwt_required()
def manage_product_current():
    current_id = get_jwt_identity()
    user = User.query.get_or_404(current_id)
    seller = Seller.query.filter_by(user_id=current_id).first()
    search = request.args.get("search") if request.args.get("search") else ""

    if request.method == "GET":
        if not seller:
            return jsonify([])
        consignments = Consignment.query.filter_by(seller_id=seller.id).all()
        products_list = []
        for consignment in consignments:
            product = Product.query.get(consignment.product_id)
            if search.lower() not in product.name.lower() or product.stock == -1:
                continue
            product_data = {
                "id": product.id,
                "name": product.name,
                "image_url": product.image_url,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "condition": product.condition,
                "consignment_id": consignment.id,
            }
            products_list.append(product_data)
        return jsonify(products_list)

    if request.method == "POST":
        if not seller:
            new_seller = Seller(
                id=None,
                user_id=current_id,
                seller_balance=0,
                bank="",
                bank_number="",
                ewallet_number=user.phone_number
            )
            db.session.add(new_seller)
            db.session.commit()

        data = request.json
        new_product = Product(
            id=None,
            name=data["name"],
            image_url=data["image_url"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"],
            condition=data["condition"]
        )

        seller = Seller.query.filter_by(user_id=current_id).first()
        consignment = Consignment(
            id=None,
            product=new_product,
            seller=seller,
        )
        db.session.add(new_product)
        db.session.add(consignment)
        db.session.commit()

        return jsonify({"message": "Product added successfully"})




