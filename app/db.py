import psycopg
from app import app

def get_db_connection():
    try:
        conn = psycopg.connect(
            host = app.config['DB_SERVER'],
            user = app.config['DB_USER'],
            password = app.config['DB_PASSWORD'],
            dbname = app.config['DB_NAME'],
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}" )
        return None
def close_db_connection(conn):
    if conn:
        conn.close()