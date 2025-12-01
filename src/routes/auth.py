from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import uuid
from supabase_service import get_user_by_email, add_user, get_user_by_email_and_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        return jsonify({"error": "Missing email, password, or username"}), 400

    try:
        new_user = add_user(email, password, username)
        
        if not new_user:
            return jsonify({"error": "User with this email already exists"}), 409

        return jsonify({"message": "User registered successfully", "user_id": new_user['id']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        # Fetch user and check password
        user = get_user_by_email_and_password(email, password)
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # In a real app, you would generate a JWT here. 
        # For this simple API, we return basic user info.
        return jsonify({
            "message": "Login successful",
            "user_id": user['id'],
            "username": user['username'],
            "is_admin": user['is_admin'],
            "is_subscribed": user.get('is_subscribed', False), # Include subscription status
            # Mock token for frontend
            "token": str(uuid.uuid4()) 
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
