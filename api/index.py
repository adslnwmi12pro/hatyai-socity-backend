import sys
import os

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

# Import Flask app
try:
    from main import app
    print(f"✓ Flask app loaded successfully")
except Exception as e:
    print(f"✗ Error loading Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

# Export for Vercel
def handler(request, response):
    return app(request, response)

# For Vercel Python runtime
app = app
