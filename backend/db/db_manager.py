import psycopg2
from psycopg2.extras import RealDictCursor
from backend.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn


def get_data_from_table(table_name: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(f"SELECT * FROM {table_name} ORDER BY registered_value DESC LIMIT 100;")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data
