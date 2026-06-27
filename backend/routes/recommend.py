from flask import Blueprint, request, jsonify
import jwt
import json
from db.connection import get_connection
from config import SECRET_KEY
from ml.predictor import predict_career
from ml.predictor import predict_career
from ml.career_data import get_career_data

recommend_bp = Blueprint('recommend', __name__)

def get_user_id(request) -> int | None:
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    try:
        payload = jwt.decode(auth.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except Exception:
        return None


@recommend_bp.route('/predict', methods=['POST'])
def predict():
    user_id = get_user_id(request)
    if not user_id:
        return jsonify({'error': 'Unauthorised.'}), 401

    data           = request.get_json()
    education      = data.get('education', '')
    specialization = data.get('specialization', '')
    skills         = data.get('skills', [])
    interest       = data.get('interest', '')
    certifications = data.get('certifications', [])
    cgpa           = float(data.get('cgpa', 60))

    if not education or not skills or not interest:
        return jsonify({'error': 'Education, skills and interest are required.'}), 400

    result = predict_career(education, specialization, skills, interest, certifications, cgpa)

    # Save to DB
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO recommendations
               (user_id, education_level, specialization, skills, interest,
                certifications, cgpa, predicted_career, confidence, top_matches, explanation)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                user_id,
                education,
                specialization,
                json.dumps(skills),
                interest,
                json.dumps(certifications),
                cgpa,
                result['predicted_career'],
                result['confidence'],
                json.dumps(result['top_matches']),
                result['explanation']
            )
        )
        conn.commit()
        rec_id = cursor.lastrowid
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        'id'              : rec_id,
        'predicted_career': result['predicted_career'],
        'confidence'      : result['confidence'],
        'top_matches'     : result['top_matches'],
        'matched_skills'  : result['matched_skills'],
        'missing_skills'  : result['missing_skills'],
        'explanation'     : result['explanation'],
        'career_info'     : result['career_info']
    })


@recommend_bp.route('/history', methods=['GET'])
def history():
    user_id = get_user_id(request)
    if not user_id:
        return jsonify({'error': 'Unauthorised.'}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT id, education_level, specialization, skills, interest,
                      certifications, cgpa, predicted_career, confidence,
                      top_matches, explanation, created_at
               FROM recommendations
               WHERE user_id = %s
               ORDER BY created_at DESC""",
            (user_id,)
        )
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    for r in rows:
        r['skills']         = json.loads(r['skills'])         if r['skills']         else []
        r['certifications'] = json.loads(r['certifications']) if r['certifications'] else []
        r['top_matches']    = json.loads(r['top_matches'])    if r['top_matches']    else []
        r['created_at']     = r['created_at'].isoformat()     if r.get('created_at') else ''
        r['career_info']    = get_career_data(r['predicted_career'])

    return jsonify({'history': rows})


@recommend_bp.route('/history/<int:rec_id>', methods=['GET'])
def history_detail(rec_id):
    user_id = get_user_id(request)
    if not user_id:
        return jsonify({'error': 'Unauthorised.'}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM recommendations WHERE id = %s AND user_id = %s",
            (rec_id, user_id)
        )
        row = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not row:
        return jsonify({'error': 'Not found.'}), 404

    row['skills']         = json.loads(row['skills'])         if row['skills']         else []
    row['certifications'] = json.loads(row['certifications']) if row['certifications'] else []
    row['top_matches']    = json.loads(row['top_matches'])    if row['top_matches']    else []
    row['created_at']     = row['created_at'].isoformat()     if row.get('created_at') else ''
    row['career_info']    = get_career_data(row['predicted_career'])

    return jsonify({'recommendation': row})
