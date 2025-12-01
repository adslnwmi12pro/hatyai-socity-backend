import os
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

# --- Supabase Initialization ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print(f"INFO: Supabase client initialized with URL: {SUPABASE_URL}")

# --- Helper Functions ---

def get_username_by_id(user_id):
    try:
        response = supabase.table('users').select('username').eq('id', user_id).execute()
        if response.data:
            return response.data[0]['username']
        return "Unknown User"
    except Exception as e:
        print(f"Error in get_username_by_id: {e}")
        return "Unknown User"

# --- User Functions ---

def get_all_users():
    try:
        response = supabase.table('users').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Error in get_all_users: {e}")
        return []

def get_user_by_id(user_id):
    try:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in get_user_by_id: {e}")
        return None

def get_user_by_email(email):
    try:
        response = supabase.table('users').select('*').eq('email', email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in get_user_by_email: {e}")
        return None

def get_user_by_email_and_password(email, password):
    try:
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    except Exception as e:
        print(f"Error in get_user_by_email_and_password: {e}")
        return None

def add_user(email, password, username, is_admin=False, is_subscribed=False):
    try:
        hashed_password = generate_password_hash(password)
        new_user = {
            'email': email,
            'password': hashed_password,
            'username': username,
            'is_admin': is_admin,
            'is_subscribed': is_subscribed
        }
        response = supabase.table('users').insert(new_user).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in add_user: {e}")
        return None

def update_user_subscription(user_id, is_subscribed):
    try:
        response = supabase.table('users').update({'is_subscribed': is_subscribed}).eq('id', user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in update_user_subscription: {e}")
        return None

# --- Incident Functions ---

def get_all_incidents():
    try:
        response = supabase.table('incidents').select('*').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error in get_all_incidents: {e}")
        return []

def get_incident_by_id(incident_id):
    try:
        response = supabase.table('incidents').select('*').eq('id', incident_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in get_incident_by_id: {e}")
        return None

def add_incident(user_id, title, description, latitude, longitude, category):
    try:
        new_incident = {
            'user_id': user_id,
            'title': title,
            'description': description,
            'latitude': latitude,
            'longitude': longitude,
            'category': category,
            'status': 'pending'
        }
        response = supabase.table('incidents').insert(new_incident).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in add_incident: {e}")
        return None

def update_incident_status(incident_id, status):
    try:
        response = supabase.table('incidents').update({'status': status}).eq('id', incident_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in update_incident_status: {e}")
        return None

def delete_incident(incident_id):
    try:
        response = supabase.table('incidents').delete().eq('id', incident_id).execute()
        return True
    except Exception as e:
        print(f"Error in delete_incident: {e}")
        return False

# --- Comment Functions ---

def get_comments_by_incident_id(incident_id):
    try:
        response = supabase.table('comments').select('*').eq('incident_id', incident_id).order('created_at', desc=False).execute()
        return response.data
    except Exception as e:
        print(f"Error in get_comments_by_incident_id: {e}")
        return []

def add_comment(incident_id, user_id, content):
    try:
        new_comment = {
            'incident_id': incident_id,
            'user_id': user_id,
            'content': content
        }
        response = supabase.table('comments').insert(new_comment).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error in add_comment: {e}")
        return None


# Alias functions for compatibility
def get_active_incidents():
    return get_all_incidents()

def create_incident(user_id, title, description, latitude, longitude, category):
    return add_incident(user_id, title, description, latitude, longitude, category)


def get_comments_by_incident(incident_id):
    return get_comments_by_incident_id(incident_id)

def create_comment(incident_id, user_id, content):
    return add_comment(incident_id, user_id, content)
