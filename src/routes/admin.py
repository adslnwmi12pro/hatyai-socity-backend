from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os

admin_bp = Blueprint("admin", __name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Helper to check if user is admin (this would be more robust with JWT claims in a real app)
def is_admin(user_id):
    try:
        response = supabase.table("users").select("is_admin").eq("id", user_id).single().execute()
        return response.data and response.data["is_admin"]
    except Exception:
        return False

@admin_bp.route("/admin/users", methods=["GET"])
def get_all_users():
    # In a real application, you would verify admin status via JWT or session
    # For simplicity, we'll assume an admin_id is passed for now
    admin_id = request.args.get("admin_id") # This is a placeholder for actual auth
    if not is_admin(admin_id):
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    try:
        response = supabase.table("users").select("id, email, username, is_admin, subscription_status, created_at").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/users/<user_id>", methods=["PUT"])
def update_user_status(user_id):
    admin_id = request.args.get("admin_id") # Placeholder
    if not is_admin(admin_id):
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    data = request.get_json()
    try:
        response = supabase.table("users").update(data).eq("id", user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/pokemons", methods=["GET"])
def get_all_pokemons_admin():
    admin_id = request.args.get("admin_id") # Placeholder
    if not is_admin(admin_id):
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    try:
        response = supabase.table("pokemons").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/comments", methods=["GET"])
def get_all_comments_admin():
    admin_id = request.args.get("admin_id") # Placeholder
    if not is_admin(admin_id):
        return jsonify({"error": "Unauthorized: Admin access required"}), 403

    try:
        response = supabase.table("comments").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

