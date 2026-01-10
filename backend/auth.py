import mysql.connector
import hashlib
import re
import os
from dotenv import load_dotenv
import requests
import secrets
import google.auth.transport.requests
from google.oauth2 import id_token

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
    # Allow login using either username or email so both auth flows map to same account
    cursor.execute(
        "SELECT id,email FROM users WHERE (username=%s OR email=%s) AND password_hash=%s",
        (username, username, hash_password(password))
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
def google_login():
    """Returns Google OAuth URL - EXACT MATCH for Google Console"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    state = secrets.token_urlsafe(16)
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri=http://127.0.0.1:8000/auth/callback&scope=openid%20email%20profile&response_type=code&state={state}"
    return auth_url

def google_callback(code):
    """Exchange Google code for user info - FIXED"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://127.0.0.1:8000/auth/callback",  # ← EXACT SAME
        "grant_type": "authorization_code",
        "code": code
    }
    
    token_response = requests.post("https://oauth2.googleapis.com/token", data=token_data).json()
    id_token_str = token_response["id_token"]
    
    user_info = id_token.verify_oauth2_token(id_token_str, google.auth.transport.requests.Request(), client_id)
    return {
        "email": user_info["email"],
        "name": user_info["name"],
        "google_id": user_info["sub"]
    }

def save_google_user(user_info):
    """Save/update Google user in DB"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Upsert Google user (email as username for consistency)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE username=%s
        """, (user_info["email"], user_info["email"], "google_auth", user_info["email"]))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()