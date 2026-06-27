import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import json
import os

print("[INFO] Loading large synthetic dataset...")
df = pd.read_excel('ml/career_dataset_large.xlsx')

print(f"[INFO] Dataset loaded with {len(df)} rows.")

# Preprocessing
df['Education Level'].fillna('Unknown', inplace=True)
df['Specialization'].fillna('Unknown', inplace=True)
df['Skills'].fillna('', inplace=True)
df['Interest'].fillna('Unknown', inplace=True)
df['Certifications'].fillna('None', inplace=True)
df['CGPA'].fillna(df['CGPA'].mean(), inplace=True)

# Encode CGPA as 0-1
df['cgpa_norm'] = df['CGPA'] / 10.0

le_edu = LabelEncoder()
le_spec = LabelEncoder()
le_int = LabelEncoder()

df['edu_enc'] = le_edu.fit_transform(df['Education Level'])
df['spec_enc'] = le_spec.fit_transform(df['Specialization'])
df['int_enc'] = le_int.fit_transform(df['Interest'])

# One-hot encoding for skills
all_skills = set()
for s_list in df['Skills'].dropna():
    for s in s_list.split(','):
        s = s.strip()
        if s:
            all_skills.add(s)
all_skills = sorted(list(all_skills))

for skill in all_skills:
    df[f'sk__{skill}'] = df['Skills'].apply(lambda x: 1 if skill in str(x) else 0)

# One-hot encoding for Certifications
all_certs = set()
for c_list in df['Certifications'].dropna():
    for c in str(c_list).split(','):
        c = c.strip()
        if c:
            all_certs.add(c)
all_certs = sorted(list(all_certs))

for cert in all_certs:
    df[f'ct__{cert}'] = df['Certifications'].apply(lambda x: 1 if cert in str(x) else 0)

feat_cols = ['edu_enc', 'spec_enc', 'int_enc', 'cgpa_norm'] + \
            [f'sk__{s}' for s in all_skills] + \
            [f'ct__{c}' for c in all_certs]

X = df[feat_cols]
y = df['Career Options']

print("[INFO] Training Random Forest model with 50+ classes...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("[INFO] Saving models...")
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/career_model.pkl')
joblib.dump(le_edu, 'models/le_edu.pkl')
joblib.dump(le_spec, 'models/le_spec.pkl')
joblib.dump(le_int, 'models/le_int.pkl')

feature_info = {
    'all_skills': all_skills,
    'all_certs': all_certs,
    'feat_cols': feat_cols
}
with open('models/feature_info.json', 'w') as f:
    json.dump(feature_info, f)

print("[OK] Training complete. Models saved.")
