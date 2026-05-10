import os
from psycopg.rows import dict_row
import psycopg
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-this'
    
    # PostgreSQL Configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_NAME = os.environ.get('DB_NAME', 'hospital_management')
    DB_PORT = os.environ.get('DB_PORT', '5432')

def get_db_connection():
    conn = psycopg.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dbname=Config.DB_NAME,
        port=Config.DB_PORT,
        row_factory=dict_row
    )
    return conn
