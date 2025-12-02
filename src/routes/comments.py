from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os

comment_bp = Blueprint("comment", __name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@comment_bp.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    user_id = data.get("user_id")
    pokemon_id = data.get("pokemon_id")
    comment_text = data.get("comment_text")

    if not all([user_id, pokemon_id, comment_text]):
        return jsonify({"error": "User ID, Pokemon ID, and comment text are required"}), 400

    try:
        response = supabase.table("comments").insert({
            "user_id": user_id,
            "pokemon_id": pokemon_id,
            "comment_text": comment_text
        }).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comment_bp.route("/comments", methods=["GET"])
def get_comments():
    try:
        pokemon_id = request.args.get("pokemon_id")
        if pokemon_id:
            response = supabase.table("comments").select("*").eq("pokemon_id", pokemon_id).order("created_at", desc=True).execute()
        else:
            response = supabase.table("comments").select("*").order("created_at", desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

