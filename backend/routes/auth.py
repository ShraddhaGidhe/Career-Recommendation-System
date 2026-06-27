from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from db.connection import get_connection
from config import SECRET_KEY, JWT_EXPIRY_DAYS

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXPIRY_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name     = (data.get('name', '') or '').strip()
    email    = (data.get('email', '') or '').strip().lower()
    password = (data.get('password', '') or '').strip()

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required.'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters.'}), 400

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered.'}), 409

        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, pw_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    token = generate_token(user_id)
    return jsonify({
        'message': 'Registration successful.',
        'token': token,
        'user': {'id': user_id, 'name': name, 'email': email}
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data     = request.get_json()
    email    = (data.get('email', '') or '').strip().lower()
    password = (data.get('password', '') or '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not user or not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return jsonify({'error': 'Invalid email or password.'}), 401

    token = generate_token(user['id'])
    return jsonify({
        'message': 'Login successful.',
        'token': token,
        'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}
    })


@auth_bp.route('/profile', methods=['GET'])
def profile():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorised.'}), 401
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token.'}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (payload['user_id'],))
        user = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not user:
        return jsonify({'error': 'User not found.'}), 404

    if user.get('created_at'):
        user['created_at'] = user['created_at'].isoformat()

    return jsonify({'user': user})
