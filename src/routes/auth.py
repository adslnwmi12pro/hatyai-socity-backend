from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os

auth_bp = Blueprint("auth", __name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password or not username:
        return jsonify({"error": "Email, password, and username are required"}), 400

    try:
        # Supabase auth signup
        user_response = supabase.auth.sign_up({"email": email, "password": password})
        user = user_response.user

        if user:
            # Insert user data into our 'users' table
            supabase.table("users").insert({"id": user.id, "email": email, "username": username}).execute()
            return jsonify({"message": "User created successfully", "user_id": user.id}), 201
        else:
            return jsonify({"error": user_response.error.message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = user_response.user
        if user:
            return jsonify({"message": "Logged in successfully", "user": user.model_dump()}), 200
        else:
            return jsonify({"error": user_response.error.message}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

