"""
predictor.py — Load trained model and predict career from user inputs
"""
import joblib
import json
import numpy as np
import pandas as pd
import os

# ── Globals (loaded once on first call) ───────────────────────────────────────
_model        = None
_le_edu       = None
_le_spec      = None
_le_int       = None
_feature_info = None

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')

def load_model():
    global _model, _le_edu, _le_spec, _le_int, _feature_info
    _model   = joblib.load(os.path.join(MODELS_DIR, 'career_model.pkl'))
    _le_edu  = joblib.load(os.path.join(MODELS_DIR, 'le_edu.pkl'))
    _le_spec = joblib.load(os.path.join(MODELS_DIR, 'le_spec.pkl'))
    _le_int  = joblib.load(os.path.join(MODELS_DIR, 'le_int.pkl'))
    with open(os.path.join(MODELS_DIR, 'feature_info.json'), 'r') as f:
        _feature_info = json.load(f)
        print("[OK] ML model loaded.")


def _safe_encode(encoder, value: str) -> int:
    """Encode a value; fall back to 0 if unseen."""
    classes = list(encoder.classes_)
    # exact match
    if value in classes:
        return int(encoder.transform([value])[0])
    # case-insensitive match
    for cls in classes:
        if cls.lower() == value.lower():
            return int(encoder.transform([cls])[0])
    return 0


def _generate_explanation(career: str, matched: list, interest: str, work_style: str, confidence: float) -> str:
    parts = []
    if matched:
        parts.append(f"your skills in {', '.join(matched[:3])}")
    if interest:
        parts.append(f"your interest in {interest}")
    if work_style:
        parts.append(f"your {work_style.lower()} work style preference")
    reason = ' and '.join(parts) if parts else 'your overall profile'
    return (
        f"Based on {reason}, {career} is your best career match "
        f"with a confidence score of {confidence:.1f}%. "
        f"This recommendation aligns with the skills and interests "
        f"most valued in the {career} domain."
    )


def predict_career(education: str, specialization: str, skills: list,
                   interest: str, certifications: list, cgpa: float) -> dict:
    global _model, _feature_info

    if _model is None:
        load_model()

    # ── Encode categorical inputs ──────────────────────────────────────────────
    edu_enc  = _safe_encode(_le_edu,  education)
    spec_enc = _safe_encode(_le_spec, specialization)
    int_enc  = _safe_encode(_le_int,  interest)
    cgpa_norm = float(cgpa) / 10.0

    row = {
        'edu_enc' : edu_enc,
        'spec_enc': spec_enc,
        'int_enc' : int_enc,
        'cgpa_norm': cgpa_norm
    }

    # ── One-hot skills ─────────────────────────────────────────────────────────
    skills_lower = [s.lower() for s in skills]
    for skill in _feature_info['all_skills']:
        row[f'sk__{skill}'] = 1 if skill.lower() in skills_lower else 0

    # ── One-hot certifications ─────────────────────────────────────────────────
    certs_lower = [c.lower() for c in certifications]
    for cert in _feature_info['all_certs']:
        row[f'ct__{cert}'] = 1 if cert.lower() in certs_lower else 0

    X = pd.DataFrame([row])[_feature_info['feat_cols']]

    # ── Predict probabilities ──────────────────────────────────────────────────
    proba   = _model.predict_proba(X)[0]
    classes = _model.classes_

    # Top 3 careers
    top_idx = np.argsort(proba)[::-1][:3]
    top_matches = [
        {'career': classes[i], 'confidence': round(float(proba[i]) * 100, 1)}
        for i in top_idx
    ]

    best_career     = top_matches[0]['career']
    best_confidence = top_matches[0]['confidence']

    # ── Matched / missing skills for top career ────────────────────────────────
    from ml.career_data import get_career_data
    career_info    = get_career_data(best_career)
    required       = career_info.get('required_skills', [])
    matched_skills = [s for s in skills if any(s.lower() == r.lower() for r in required)]
    missing_skills = [r for r in required if not any(r.lower() == s.lower() for s in skills)]

    explanation = _generate_explanation(
        best_career, matched_skills, interest, '', best_confidence
    )

    return {
        'predicted_career' : best_career,
        'confidence'       : best_confidence,
        'top_matches'      : top_matches,
        'matched_skills'   : matched_skills,
        'missing_skills'   : missing_skills,
        'explanation'      : explanation,
        'career_info'      : career_info
    }
