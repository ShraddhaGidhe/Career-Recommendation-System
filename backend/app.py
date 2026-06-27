from flask import Flask, jsonify
from flask_cors import CORS
from config import SECRET_KEY
from db.connection import init_db
from ml.predictor import load_model
from routes.auth import auth_bp
from routes.recommend import recommend_bp
from routes.roadmap import roadmap_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

# Register blueprints
app.register_blueprint(auth_bp,       url_prefix='/api/auth')
app.register_blueprint(recommend_bp,  url_prefix='/api/recommend')
app.register_blueprint(roadmap_bp,    url_prefix='/api/roadmap')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Career Recommendation API is running 🚀'})

if __name__ == '__main__':
    print("[INFO] Initialising database...")
    init_db()
    print("[INFO] Loading ML model...")
    load_model()
    print("[INFO] Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
