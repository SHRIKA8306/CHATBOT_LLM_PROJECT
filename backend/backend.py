import os
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import mysql.connector
from groq import Groq
from auth import register_user, authenticate_user

# ✅ Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME   = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY is missing in .env file")

client = Groq(api_key=GROQ_API_KEY)

# ✅ Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "2501"),
        database=os.getenv("MYSQL_DATABASE", "chatbot_db"),
        auth_plugin="mysql_native_password"
    )



# ✅ Ensure table exists
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
    # Add user column if it doesn't exist (for backward compatibility)
    try:
        cursor.execute("ALTER TABLE chat_history ADD COLUMN user VARCHAR(255)")
    except mysql.connector.Error as e:
        if e.errno != 1060:  # Column already exists
            print(f"Error adding user column: {e}")
    conn.commit()
    cursor.close()
    conn.close()


ensure_table_exists()


@app.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JSONResponse(status_code=400, content={"error": "Username, email, and password required"})

        if register_user(username, email, password):
            return {"message": "User registered successfully"}
        else:
            return JSONResponse(status_code=400, content={"error": "Username or email already exists"})
    except Exception as e:
        print("🔥 ERROR in /register:", e)
        return JSONResponse(status_code=500, content={"error": "Server error"})


@app.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JSONResponse(status_code=400, content={"error": "Username and password required"})

        user = authenticate_user(username, password)
        if user:
            return {"message": "Login successful", "user_id": user[0], "email": user[1]}
        else:
            return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
    except Exception as e:
        print("🔥 ERROR in /login:", e)
        return JSONResponse(status_code=500, content={"error": "Server error"})


@app.get("/chat_history/{username}")
async def get_chat_history(username: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_message, bot_reply, timestamp 
            FROM chat_history 
            WHERE user = %s 
            ORDER BY timestamp DESC 
            LIMIT 50
        """, (username,))
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Format the response
        formatted_history = []
        if history:
            for chat in history:
                timestamp_str = chat[3].isoformat() if chat[3] else None
                formatted_history.append({
                    "id": chat[0],
                    "user_message": chat[1],
                    "bot_reply": chat[2],
                    "timestamp": timestamp_str
                })
        
        return {"chat_history": formatted_history}
    except Exception as e:
        print("🔥 ERROR in /chat_history:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "Server error"})


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_msg = data.get("message", "")
        user = data.get("user", "anonymous")

        if not user_msg:
            return JSONResponse(status_code=400, content={"error": "Message missing"})

        # ✅ Create connection per request
        conn = get_connection()
        cursor = conn.cursor()

        # Save user message
        cursor.execute("INSERT INTO chat_history (user, user_message) VALUES (%s, %s)", (user, user_msg))
        chat_id = cursor.lastrowid
        conn.commit()

        # ✅ Call Groq LLM
        def send_to_groq(user_msg: str) -> str:
            prompt = f"""
            You are a Women's Safety Assistant. ONLY answer questions related to women's safety in India.
            Include: safety tips, Indian laws, emergency numbers, and helplines.
            If the question is unrelated, reply: "Sorry, I can only answer questions about women's safety."

            User Question: {user_msg}
            """
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content or ""
        bot_reply = send_to_groq(user_msg)

        # ✅ Save bot reply
        cursor.execute("UPDATE chat_history SET bot_reply = %s WHERE id = %s", (bot_reply, chat_id))
        conn.commit()

        cursor.close()
        conn.close()

        return {"reply": bot_reply}

    except Exception as e:
        print("🔥 ERROR in /chat:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": "Server error. Check backend logs"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
