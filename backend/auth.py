import mysql.connector
import hashlib
import re
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        auth_plugin="mysql_native_password"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Must include uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Must include lowercase letter"
    if not re.search(r"\d", password):
        return False, "Must include number"
    if not re.search(r"[!@#$%^&*]", password):
        return False, "Must include special character"
    return True, "Strong password"

def register_user(username, email, password):
    strong, msg = is_strong_password(password)
    if not strong:
        return False, msg
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username,email,password_hash) VALUES (%s,%s,%s)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True, "Registered successfully"
    except mysql.connector.IntegrityError:
        return False, "Username or email already exists"
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id,email FROM users WHERE username=%s AND password_hash=%s",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def reset_password(username, new_password):
    strong, msg = is_strong_password(new_password)
    if not strong:
        return False, msg
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return False, "Username does not exist"
    cursor.execute(
        "UPDATE users SET password_hash=%s WHERE username=%s",
        (hash_password(new_password), username)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Password reset successfully"
