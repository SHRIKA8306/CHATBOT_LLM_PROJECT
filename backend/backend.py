import os
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import mysql.connector
from groq import Groq

# ✅ Load environment variables
load_dotenv()

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
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "chatbot_db"),
    )


# ✅ Ensure table exists
def ensure_table_exists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_message TEXT,
            bot_reply TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


ensure_table_exists()


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_msg = data.get("message", "")

        if not user_msg:
            return JSONResponse(status_code=400, content={"error": "Message missing"})

        # ✅ Create connection per request
        conn = get_connection()
        cursor = conn.cursor()

        # Save user message
        cursor.execute("INSERT INTO chat_history (user_message) VALUES (%s)", (user_msg,))
        chat_id = cursor.lastrowid
        conn.commit()

        # ✅ Call Groq LLM
        response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": user_msg}],
)

        bot_reply = response.choices[0].message.content

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
