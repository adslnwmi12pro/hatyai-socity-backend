from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": ["https://hatyai-socity-fast-frontend.vercel.app", "http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Import and register blueprints
try:
    from routes.auth import auth_bp
    from routes.pokemons import pokemon_bp
    from routes.comments import comment_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pokemon_bp, url_prefix="/api")
    app.register_blueprint(comment_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
except ImportError as e:
    print(f"Warning: Could not import routes: {e}")

# Basic route for testing
@app.route('/')
def index():
    return jsonify({
        "message": "Welcome to KitPokeMap Backend API!",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
