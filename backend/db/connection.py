import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG

connection_pool = None

def init_pool():
    global connection_pool
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="career_pool",
        pool_size=5,
        **DB_CONFIG
    )

def get_connection():
    global connection_pool
    if connection_pool is None:
        init_pool()
    return connection_pool.get_connection()

def init_db():
    import os

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    with open(schema_path, 'r') as f:
        sql_script = f.read()

    for stmt in sql_script.split(';'):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)

    conn.commit()
    cursor.close()
    conn.close()

    print("[OK] Database initialized successfully.")
    init_pool()