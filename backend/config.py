import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "career_db"),
}

SECRET_KEY = os.getenv('SECRET_KEY', 'career_recommendation_secret_key_2026')
JWT_EXPIRY_DAYS = 7
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
