import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with proper configuration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000", "http://localhost:5174", "https://hatyai-socity-fast-frontend-pj7w4r7mv.vercel.app", "https://hatyai-socity-fast-frontend-97nl176kv.vercel.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "User-Id"],
        "supports_credentials": True
    }
})

# Add a before_request handler to handle preflight requests
@app.before_request
def handle_preflight():
    from flask import request
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,User-Id")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Hatyai Socity fast Backend API", "status": "running"})

# Import and register Blueprints (routes) here
from routes.auth import auth_bp
from routes.incidents import incidents_bp
from routes.admin import admin_bp
from routes.comments import comments_bp
from routes.subscription import subscription_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(incidents_bp, url_prefix='/incidents')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(comments_bp, url_prefix='/comments')
app.register_blueprint(subscription_bp, url_prefix='/subscription')

# No mock data initialization needed - using Supabase

if __name__ == "__main__":
    # For local development only
    app.run(debug=True, port=5001)
