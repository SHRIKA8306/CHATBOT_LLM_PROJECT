import mysql.connector
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "2501"),
        database=os.getenv("MYSQL_DATABASE", "chatbot_db"),
        auth_plugin="mysql_native_password"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def register_user(username, email, password):
    password_hash = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, password_hash))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # Username or email already exists
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    password_hash = hash_password(password)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users WHERE username = %s AND password_hash = %s",
                   (username, password_hash))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user  # Returns (id, email) if authenticated, None otherwise

# Initialize the table
create_users_table()