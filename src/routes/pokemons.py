from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os

pokemon_bp = Blueprint("pokemon", __name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@pokemon_bp.route("/pokemons", methods=["POST"])
def add_pokemon():
    data = request.get_json()
    pokemon_name = data.get("pokemon_name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    reported_by = data.get("reported_by") # User ID
    expires_at = data.get("expires_at") # Optional

    if not all([pokemon_name, latitude, longitude, reported_by]):
        return jsonify({"error": "Pokemon name, latitude, longitude, and reporter are required"}), 400

    try:
        response = supabase.table("pokemons").insert({
            "pokemon_name": pokemon_name,
            "latitude": latitude,
            "longitude": longitude,
            "reported_by": reported_by,
            "expires_at": expires_at
        }).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pokemon_bp.route("/pokemons", methods=["GET"])
def get_pokemons():
    try:
        response = supabase.table("pokemons").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pokemon_bp.route("/pokemons/<pokemon_id>", methods=["GET"])
def get_pokemon(pokemon_id):
    try:
        response = supabase.table("pokemons").select("*").eq("id", pokemon_id).execute()
        if response.data:
            return jsonify(response.data[0])
        return jsonify({"message": "Pokemon not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pokemon_bp.route("/pokemons/<pokemon_id>", methods=["PUT"])
def update_pokemon(pokemon_id):
    data = request.get_json()
    try:
        response = supabase.table("pokemons").update(data).eq("id", pokemon_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pokemon_bp.route("/pokemons/<pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id):
    try:
        supabase.table("pokemons").delete().eq("id", pokemon_id).execute()
        return jsonify({"message": "Pokemon deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

