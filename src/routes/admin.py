from flask import Blueprint, request, jsonify
from supabase_service import get_user_by_id, get_all_users, get_all_incidents, get_incident_by_id, update_incident_status

admin_bp = Blueprint('admin', __name__)

# Helper function to check if user is admin (mock)
def is_admin(user_id):
    
    if not user_id:
        return False
    user = get_user_by_id(user_id)
    return user and user.get('is_admin', False)

@admin_bp.route('/users', methods=['GET'])
def get_all_users_admin():
    user_id = request.headers.get('User-Id')
    if not is_admin(user_id):
        return jsonify({"error": "Forbidden: Admin access required"}), 403

    try:
        # Return all users from data store
        # Filter out password hash for security (even though it's mock data)
        safe_users = [{k: v for k, v in user.items() if k != 'password'} for user in get_all_users()]
        return jsonify(safe_users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/incidents', methods=['GET'])
def get_all_incidents_admin():
    user_id = request.headers.get('User-Id')
    if not is_admin(user_id):
        return jsonify({"error": "Forbidden: Admin access required"}), 403

    try:
        # Return all incidents from data store
        return jsonify(get_all_incidents()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/incidents/<incident_id>/status', methods=['PUT'])
def update_incident_status(incident_id):
    user_id = request.headers.get('User-Id')
    if not is_admin(user_id):
        return jsonify({"error": "Forbidden: Admin access required"}), 403

    data = request.get_json()
    new_status = data.get('status')

    if not new_status:
        return jsonify({"error": "Missing status field"}), 400

    try:
        if update_incident_status(incident_id, new_status):
            incident = get_incident_by_id(incident_id)
            return jsonify({"message": "Incident status updated successfully", "incident": incident}), 200
        
        return jsonify({"error": "Incident not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
