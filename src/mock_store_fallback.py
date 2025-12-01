from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

# Mock Data Stores
MOCK_USERS = {}
MOCK_INCIDENTS = {}
MOCK_COMMENTS = {}

# --- Helper Functions ---

def get_username_by_id(user_id):
    user = get_user_by_id(user_id)
    return user['username'] if user else "Unknown User"

# --- User Functions ---

def get_user_by_email(email):
    return MOCK_USERS.get(email)

def get_user_by_id(user_id):
    for user in MOCK_USERS.values():
        if user['id'] == user_id:
            return user
    return None

def get_all_users():
    return list(MOCK_USERS.values())

def add_user(email, password, username):
    if get_user_by_email(email):
        return None # User already exists

    hashed_password = generate_password_hash(password)
    new_user_id = str(uuid.uuid4())
    
    new_user_data = {
        "id": new_user_id,
        "email": email,
        "password": hashed_password,
        "username": username,
        "is_admin": False,
        "is_subscribed": False,
        "created_at": datetime.now().isoformat()
    }
    
    MOCK_USERS[email] = new_user_data
    return new_user_data

def get_user_by_email_and_password(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        return user
    return None

def update_user_subscription(user_id, is_subscribed):
    for user in MOCK_USERS.values():
        if user['id'] == user_id:
            user['is_subscribed'] = is_subscribed
            return True
    return False

# --- Incident Functions ---

def get_all_incidents():
    # Sort by created_at descending
    return sorted(list(MOCK_INCIDENTS.values()), key=lambda x: x['created_at'], reverse=True)

def get_active_incidents():
    # Filter by status='active' and sort by created_at descending
    active_incidents = [inc for inc in MOCK_INCIDENTS.values() if inc['status'] == 'active']
    return sorted(active_incidents, key=lambda x: x['created_at'], reverse=True)

def get_incident_by_id(incident_id):
    return MOCK_INCIDENTS.get(incident_id)

def create_incident(user_id, type, title, description, latitude, longitude):
    new_incident_id = str(uuid.uuid4())
    
    new_incident_data = {
        "id": new_incident_id,
        "user_id": user_id,
        "type": type,
        "title": title,
        "description": description,
        "latitude": latitude,
        "longitude": longitude,
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    MOCK_INCIDENTS[new_incident_id] = new_incident_data
    return new_incident_data

def update_incident_status(incident_id, status):
    incident = get_incident_by_id(incident_id)
    if incident:
        incident['status'] = status
        return True
    return False

def delete_incident(incident_id):
    if incident_id in MOCK_INCIDENTS:
        del MOCK_INCIDENTS[incident_id]
        # Also delete related comments
        comments_to_delete = [cid for cid, comment in MOCK_COMMENTS.items() if comment['incident_id'] == incident_id]
        for cid in comments_to_delete:
            del MOCK_COMMENTS[cid]
        return True
    return False

# --- Comment Functions ---

def get_comments_by_incident(incident_id):
    # Filter by incident_id and sort by created_at ascending
    comments = [comment for comment in MOCK_COMMENTS.values() if comment['incident_id'] == incident_id]
    return sorted(comments, key=lambda x: x['created_at'], reverse=False)

def create_comment(incident_id, user_id, content):
    new_comment_id = str(uuid.uuid4())
    
    new_comment_data = {
        "id": new_comment_id,
        "incident_id": incident_id,
        "user_id": user_id,
        "content": content,
        "created_at": datetime.now().isoformat()
    }
    
    MOCK_COMMENTS[new_comment_id] = new_comment_data
    return new_comment_data

# --- Initialization ---

def initialize_mock_data():
    # Clear existing data
    MOCK_USERS.clear()
    MOCK_INCIDENTS.clear()
    MOCK_COMMENTS.clear()
    
    # 1. Admin User
    admin_email = "admin@example.com"
    admin_password = "adminpassword"
    admin_user = add_user(admin_email, admin_password, "AdminUser")
    if admin_user:
        admin_user['is_admin'] = True
        admin_user['is_subscribed'] = True
    
    # 2. Regular User
    user_email = "user@example.com"
    user_password = "userpassword"
    regular_user = add_user(user_email, user_password, "RegularUser")
    
    # 3. Incident
    incident_id = str(uuid.uuid4())
    MOCK_INCIDENTS[incident_id] = {
        "id": incident_id,
        "user_id": admin_user['id'],
        "type": "ภัยพิบัติ",
        "title": "น้ำท่วมถนนสายหลัก",
        "description": "น้ำท่วมถนนกาญจนวนิช บริเวณหน้าห้างสรรพสินค้า",
        "latitude": 7.0000,
        "longitude": 100.4700,
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    # 4. Comment
    create_comment(incident_id, regular_user['id'], "ระวังรถเล็กนะครับ! น้ำสูงจริง")
