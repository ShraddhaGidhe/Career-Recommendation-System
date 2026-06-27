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
    """Initialize database and create tables from schema.sql"""
    import os
    # First connect without specifying database to create it
    cfg = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
    conn = mysql.connector.connect(**cfg)
    cursor = conn.cursor()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        statements = f.read().split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)
    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Database initialized successfully.")
    init_pool()
