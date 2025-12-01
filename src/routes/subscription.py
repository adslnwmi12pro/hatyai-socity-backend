from flask import Blueprint, request, jsonify
from supabase_service import get_user_by_id, update_user_subscription

subscription_bp = Blueprint('subscription', __name__)

# Helper function to check if user is logged in (mock)
def is_logged_in(request):
    return request.headers.get('User-Id')

@subscription_bp.route('/status', methods=['GET'])
def get_subscription_status():
    user_id = is_logged_in(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "is_subscribed": user.get('is_subscribed', False),
        "plan": "Premium" if user.get('is_subscribed', False) else "Free"
    }), 200

@subscription_bp.route('/subscribe', methods=['POST'])
def subscribe():
    user_id = is_logged_in(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Mock payment processing
    # In a real application, this would involve a payment gateway (e.g., Stripe, Omise)
    
    # Update mock user status
    update_user_subscription(user_id, True)
    
    return jsonify({
        "message": "Subscription successful! Welcome to Premium.",
        "is_subscribed": True,
        "plan": "Premium"
    }), 200

@subscription_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    user_id = is_logged_in(request)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update mock user status
    update_user_subscription(user_id, False)
    
    return jsonify({
        "message": "Unsubscribed successfully. You are now on the Free plan.",
        "is_subscribed": False,
        "plan": "Free"
    }), 200
