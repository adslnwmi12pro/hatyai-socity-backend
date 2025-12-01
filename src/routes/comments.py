from flask import Blueprint, request, jsonify
from supabase_service import get_comments_by_incident, create_comment, get_username_by_id

comments_bp = Blueprint('comments', __name__)

# Helper function to check if user is logged in (mock)
def is_logged_in(request):
    # In a real app, this would validate a JWT token
    # For now, we rely on a 'User-Id' header for simplicity
    return request.headers.get('User-Id')

@comments_bp.route('/<incident_id>', methods=['GET'])
def get_comments(incident_id):
    try:
        # Get comments from data store
        incident_comments = [
            {
                **comment,
                "username": get_username_by_id(comment['user_id'])
            }
            for comment in get_comments_by_incident(incident_id)
        ]
        return jsonify(incident_comments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comments_bp.route('/', methods=['POST'])
def add_comment():
    user_id = is_logged_in(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    incident_id = data.get('incident_id')
    comment_text = data.get('comment_text')

    if not all([incident_id, comment_text]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_comment = create_comment(incident_id, user_id, comment_text)
        
        # Prepare response with username
        response_comment = {
            **new_comment,
            "username": get_username_by_id(user_id)
        }
        
        return jsonify({"message": "Comment added successfully", "comment": response_comment}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
