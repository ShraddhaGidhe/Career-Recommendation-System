import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'career_db')
)

cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE recommendations ADD COLUMN career_info_json JSON;")
    print("Added career_info_json")
except Exception as e:
    print(e)

try:
    cursor.execute("ALTER TABLE recommendations ADD COLUMN roadmap_json JSON;")
    print("Added roadmap_json")
except Exception as e:
    print(e)

cursor.close()
conn.close()
