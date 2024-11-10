import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict
from backend.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None


def get_data_from_table(table_name: str, parameter: str, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = f"SELECT registered_value, {parameter} FROM {table_name} WHERE 1=1"
        params = []

        if start_time:
            query += " AND registered_value >= %s"
            params.append(start_time)
        if end_time:
            query += " AND registered_value <= %s"
            params.append(end_time)

        query += " ORDER BY registered_value ASC;"
        cursor.execute(query, params)
        data = cursor.fetchall()

        return data

    except psycopg2.Error as e:
        print(f"Error fetching data: {e}")
        return []

    finally:
        cursor.close()
        conn.close()


def get_table_names():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    finally:
        cursor.close()
        conn.close()


def get_column_names(table_name: str):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
        columns = [row[0] for row in cursor.fetchall()]

        filtered_columns = [col for col in columns if col not in ('value_id', 'registered_value')]
        return filtered_columns
    finally:
        cursor.close()
        conn.close()


# – Выбор временных отрезков для построения графиков –
def get_oldest_timestamp(table_name: str) -> Optional[str]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT MIN(registered_value) FROM {table_name};")
        oldest = cursor.fetchone()[0]
        return oldest
    finally:
        cursor.close()
        conn.close()


def get_newest_timestamp(table_name: str) -> Optional[str]:
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(registered_value) FROM {table_name};")
        newest = cursor.fetchone()[0]
        return newest
    finally:
        cursor.close()
        conn.close()