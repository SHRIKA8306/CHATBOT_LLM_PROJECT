from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import register_user, authenticate_user, reset_password
from auth import google_login, google_callback, save_google_user
import mysql.connector
import os
from dotenv import load_dotenv
import traceback
from groq import Groq
import requests
from auth import google_login, google_callback, save_google_user
import urllib.parse

# ========== NEW: Import RAG functions ==========
from rag_service import retrieve_context, build_rag_prompt

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL")
client = Groq(api_key=GROQ_API_KEY)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        auth_plugin="mysql_native_password"
    )

# ----------------- TABLE -----------------
def ensure_table_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user VARCHAR(255),
            user_message TEXT,
            bot_reply TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            email VARCHAR(255) UNIQUE,
            password_hash VARCHAR(255)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

ensure_table_exists()

# ----------------- REGISTER -----------------
@app.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not username or not email or not password:
            return JSONResponse(status_code=400, content={"error":"Username, email, and password required"})
        success, msg = register_user(username,email,password)
        if success:
            return {"message": msg}
        else:
            return JSONResponse(status_code=400, content={"error": msg})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error":"Server error"})

# ----------------- LOGIN -----------------
@app.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return JSONResponse(status_code=400, content={"error":"Username and password required"})
        user = authenticate_user(username,password)
        if user:
            return {"message":"Login successful","user_id":user[0],"email":user[1]}
        else:
            return JSONResponse(status_code=401, content={"error":"Invalid credentials"})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error":"Server error"})

# ----------------- FORGOT PASSWORD -----------------
@app.post("/forgot_password")
async def forgot_password(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        new_password = data.get("new_password")
        if not username or not new_password:
            return JSONResponse(status_code=400, content={"error":"Username and new password required"})
        success, msg = reset_password(username,new_password)
        if success:
            return {"message": msg}
        else:
            return JSONResponse(status_code=400, content={"error": msg})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error":"Server error"})

# ----------------- CHAT WITH RAG -----------------
@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_msg = data.get("message","")
        user = data.get("user","anonymous")
        if not user_msg:
            return JSONResponse(status_code=400, content={"error":"Message missing"})

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_history (user,user_message) VALUES (%s,%s)", (user,user_msg))
        chat_id = cursor.lastrowid
        conn.commit()

        # ========== NEW: RAG - Retrieve relevant context ==========
        contexts = retrieve_context(user_msg, top_k=3)
        
        # Build enhanced prompt with context
        prompt = build_rag_prompt(user_msg, contexts)
        
        # LLM call with RAG context
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role":"user","content":prompt}]
        )
        bot_reply = response.choices[0].message.content or ""
        
        cursor.execute("UPDATE chat_history SET bot_reply=%s WHERE id=%s",(bot_reply,chat_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        # ========== NEW: Return context sources (optional) ==========
        return {
            "reply": bot_reply,
            "sources": [
                {
                    "text": ctx["text"][:150] + "...",
                    "type": ctx["metadata"].get("type"),
                    "relevance": round(ctx["score"], 3)
                }
                for ctx in contexts
            ]
        }
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error":"Server error"})

# ----------------- CHAT HISTORY -----------------
@app.get("/chat_history/{username}")
async def get_chat_history(username: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, user_message, bot_reply, timestamp FROM chat_history WHERE user=%s ORDER BY timestamp ASC", (username,))
        chats = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"chat_history": chats}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "Server error"})

# ----------------- GOOGLE AUTH -----------------
@app.get("/auth/google")
async def auth_google():
    """Redirect to Google OAuth"""
    return {"auth_url": google_login()}

@app.get("/auth/callback")
async def auth_google_callback(code: str):
    """Google OAuth callback - saves user and redirects"""
    try:
        user_info = google_callback(code)
        success = save_google_user(user_info)
        if success:
            username = user_info["email"]
            # Include the display name separately so frontend can show a friendly name
            display_name = user_info.get("name", "")
            redirect_url = f"http://127.0.0.1:8501/?google_login=1&user={urllib.parse.quote(username)}&name={urllib.parse.quote(display_name)}"
            return RedirectResponse(redirect_url)
        return JSONResponse(status_code=500, content={"error": "Failed to save user"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/verify-google-login")
async def verify_google_login(user: str):
    """Verify Google login success"""
    return {"message": "Login successful", "user": user, "logged_in": True}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)