from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import register_user, authenticate_user, reset_password, google_login, google_callback, save_google_user
import mysql.connector
import os
from dotenv import load_dotenv
import traceback
from groq import Groq
import urllib.parse
from rag_service import retrieve_context, build_rag_prompt

# Load environment variables
load_dotenv()

app = FastAPI(title="Women's Safety Chatbot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Validate required env vars at startup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # Default fallback
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is required")
if not all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
    raise ValueError("All MySQL env vars are required")

client = Groq(api_key=GROQ_API_KEY)

def get_connection():
    """Get MySQL connection with error handling"""
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            auth_plugin="mysql_native_password"
        )
    except mysql.connector.Error as e:
        raise Exception(f"Database connection failed: {str(e)}")

def ensure_table_exists():
    """Create required tables safely"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Table for chat threads (conversations)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_threads (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user VARCHAR(255),
                title VARCHAR(255),  # Preview of the first user message for display
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table for individual messages within a thread
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id INT,
                role ENUM('user', 'assistant'),
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chat_threads(id) ON DELETE CASCADE
            )
        """)
        
        # Keep the old table for migration (optional, or drop it after migrating data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user VARCHAR(255),
                user_message TEXT,
                bot_reply TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
    except Exception as e:
        print(f"Table creation failed: {e}")
    finally:
        if conn and conn.is_connected():
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
        if not all([username, email, password]):
            return JSONResponse(status_code=400, content={"error": "Username, email, and password required"})
        
        success, msg = register_user(username, email, password)
        if success:
            return {"message": msg}
        else:
            return JSONResponse(status_code=400, content={"error": msg})
    except Exception as e:
        print(f"Register error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Server error"})

# ----------------- LOGIN -----------------
@app.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        if not all([username, password]):
            return JSONResponse(status_code=400, content={"error": "Username and password required"})
        
        user = authenticate_user(username, password)
        if user:
            return {"message": "Login successful", "user_id": user[0], "email": user[1]}
        else:
            return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
    except Exception as e:
        print(f"Login error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Server error"})

# ----------------- FORGOT PASSWORD -----------------
@app.post("/forgot_password")
async def forgot_password(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        new_password = data.get("new_password")
        if not all([username, new_password]):
            return JSONResponse(status_code=400, content={"error": "Username and new password required"})
        
        success, msg = reset_password(username, new_password)
        if success:
            return {"message": msg}
        else:
            return JSONResponse(status_code=400, content={"error": msg})
    except Exception as e:
        print(f"Forgot password error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Server error"})

# ----------------- CHAT WITH RAG (FIXED) -----------------
@app.post("/chat")
async def chat(request: Request):
    conn = None
    cursor = None
    try:
        data = await request.json()
        user_msg = data.get("message", "")
        user = data.get("user", "anonymous")
        chat_id = data.get("chat_id")  # New: Pass chat_id from frontend if continuing a thread
        
        if not user_msg:
            return JSONResponse(status_code=400, content={"error": "Message missing"})

        conn = get_connection()
        cursor = conn.cursor()

        # If no chat_id, create a new thread
        if not chat_id:
            cursor.execute("INSERT INTO chat_threads (user, title) VALUES (%s, %s)", (user, user_msg[:50]))  # Title as first 50 chars
            chat_id = cursor.lastrowid
            conn.commit()

        # Insert the user message into messages
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s)", (chat_id, "user", user_msg))
        conn.commit()

        # RAG Pipeline with safety checks
        contexts = []
        try:
            contexts = retrieve_context(user_msg, top_k=3)
        except Exception as rag_error:
            print(f"RAG retrieval failed (continuing without context): {rag_error}")

        # Build prompt safely
        try:
            prompt = build_rag_prompt(user_msg, contexts)
        except Exception as prompt_error:
            print(f"Prompt building failed: {prompt_error}")
            prompt = f"User: {user_msg}\nAssistant:"

        # Groq LLM call
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        bot_reply = response.choices[0].message.content or "Sorry, I couldn't generate a response."

        # Insert the assistant reply into messages
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s)", (chat_id, "assistant", bot_reply))
        conn.commit()

        # Build safe sources response
        sources = []
        for ctx in contexts[:3]:  # Limit to top 3
            try:
                source = {
                    "text": (ctx.get("text") or "")[:150] + "..." if ctx.get("text") else "N/A",
                    "type": ctx.get("metadata", {}).get("type", "unknown"),
                    "relevance": round(ctx.get("score", 0), 3)
                }
                sources.append(source)
            except Exception:
                continue

        return {
            "reply": bot_reply,
            "sources": sources,
            "chat_id": chat_id
        }

    except Exception as e:
        print(f"Chat endpoint error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Chat service unavailable"})
    
    finally:
        # Always cleanup database resources
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ----------------- CHAT HISTORY -----------------
@app.get("/chat_history/{username}")
async def get_chat_history(username: str):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get chat threads for the user
        cursor.execute(
            "SELECT id, title, created_at FROM chat_threads WHERE user = %s ORDER BY created_at DESC", 
            (username,)
        )
        threads = cursor.fetchall()
        
        # For each thread, get the messages (optional: limit to first few for preview)
        for thread in threads:
            cursor.execute(
                "SELECT role, content FROM messages WHERE chat_id = %s ORDER BY timestamp ASC",
                (thread["id"],)
            )
            thread["messages"] = cursor.fetchall()  # Full messages for loading
        
        return {"chat_history": threads}
    except Exception as e:
        print(f"Chat history error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Failed to fetch history"})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ----------------- GOOGLE AUTH -----------------
@app.get("/auth/google")
async def auth_google():
    """Returns Google OAuth URL for frontend redirect"""
    return {"auth_url": google_login()}

@app.get("/auth/callback")
async def auth_google_callback(code: str):
    """Google OAuth callback"""
    try:
        user_info = google_callback(code)
        success = save_google_user(user_info)
        if success:
            username = user_info["email"]
            display_name = user_info.get("name", username)
            # Redirect to Streamlit frontend
            redirect_url = (
                f"http://127.0.0.1:8501/"
                f"?google_login=1&user={urllib.parse.quote(username)}"
                f"&name={urllib.parse.quote(display_name)}"
            )
            return RedirectResponse(redirect_url)
        return JSONResponse(status_code=500, content={"error": "Failed to save Google user"})
    except Exception as e:
        print(f"Google callback error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/verify-google-login")
async def verify_google_login(user: str):
    return {"message": "Login successful", "user": user, "logged_in": True}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": GROQ_MODEL}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)