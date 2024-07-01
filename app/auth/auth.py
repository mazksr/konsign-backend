from app import app
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models.User import User

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        if user.is_admin:
            access_token = create_access_token(identity=user.id, expires_delta=False)
        else:
            access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login success", "access_token": access_token}), 200
    else:
        return jsonify({"message": "Email atau password salah."}), 466


@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_id).first()
    print(current_user, current_user.id)
    return jsonify(logged_in_as=current_user.username, is_admin=current_user.is_admin), 200
