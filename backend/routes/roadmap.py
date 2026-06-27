from flask import Blueprint, request, jsonify
import jwt
from db.connection import get_connection
from config import SECRET_KEY
from ml.career_data import get_career_data

roadmap_bp = Blueprint('roadmap', __name__)

def get_user_id(request) -> int | None:
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    try:
        payload = jwt.decode(auth.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except Exception:
        return None


@roadmap_bp.route('/<path:career_name>', methods=['GET'])
def get_roadmap(career_name):
    user_id = get_user_id(request)
    if not user_id:
        return jsonify({'error': 'Unauthorised.'}), 401

    career_info = get_career_data(career_name)
    if not career_info.get('roadmap'):
        return jsonify({'error': 'Career not found.'}), 404

    # Get user's saved progress for this career
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT skill_name, status FROM user_roadmaps WHERE user_id = %s AND career_name = %s",
            (user_id, career_name)
        )
        progress_rows = cursor.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    progress_map = {r['skill_name']: r['status'] for r in progress_rows}

    # Attach progress to each roadmap skill
    roadmap_with_progress = []
    for item in career_info['roadmap']:
        skill = item['skill']
        roadmap_with_progress.append({
            **item,
            'status': progress_map.get(skill, 'Not Started')
        })

    completed = sum(1 for r in roadmap_with_progress if r['status'] == 'Completed')
    total     = len(roadmap_with_progress)
    progress_pct = round((completed / total) * 100) if total > 0 else 0

    return jsonify({
        'career'      : career_name,
        'career_info' : career_info,
        'roadmap'     : roadmap_with_progress,
        'progress_pct': progress_pct,
        'completed'   : completed,
        'total'       : total
    })


@roadmap_bp.route('/progress/update', methods=['POST'])
def update_progress():
    user_id = get_user_id(request)
    if not user_id:
        return jsonify({'error': 'Unauthorised.'}), 401

    data        = request.get_json()
    career_name = data.get('career_name', '')
    skill_name  = data.get('skill_name', '')
    status      = data.get('status', 'Not Started')

    if status not in ('Not Started', 'Learning', 'Completed'):
        return jsonify({'error': 'Invalid status.'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO user_roadmaps (user_id, career_name, skill_name, status)
               VALUES (%s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE status = %s""",
            (user_id, career_name, skill_name, status, status)
        )
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': 'Progress updated.', 'status': status})


@roadmap_bp.route('/progress/all', methods=['GET'])
def all_progress():
    user_id = get_user_id(request)
    if not user_id:
        return jsonify({'error': 'Unauthorised.'}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT career_name, skill_name, status, updated_at
               FROM user_roadmaps WHERE user_id = %s ORDER BY career_name, updated_at DESC""",
            (user_id,)
        )
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    for r in rows:
        if r.get('updated_at'):
            r['updated_at'] = r['updated_at'].isoformat()

    return jsonify({'progress': rows})
