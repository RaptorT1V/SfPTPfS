import os

DB_NAME = os.getenv("DB_NAME", "diagnostics_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

'''
DB_NAME = "diagnostics_db"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
'''