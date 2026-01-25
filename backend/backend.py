from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import (
    register_user,
    authenticate_user,
    reset_password,
    google_login,
    google_callback,
    save_google_user
)
import mysql.connector
import os
import traceback
import urllib.parse
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from dotenv import load_dotenv
from google import genai
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")

# Ensure model has correct format for new SDK
if not GEMINI_MODEL.startswith("models/"):
    GEMINI_MODEL = f"models/{GEMINI_MODEL}"

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is required")
if not all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]):
    raise ValueError("All MySQL env vars are required")

# Configure Gemini with new API
client = genai.Client(api_key=GEMINI_API_KEY)


# ========== SYSTEM PROMPT - ROLE & BEHAVIOR ==========
SYSTEM_PROMPT = """# PERSONA
You are an expert Women's Safety Assistant specializing in Indian legal frameworks, women's rights, and support systems. You provide accurate, empathetic, and actionable information to help women navigate safety concerns, legal rights, and support resources. Your tone is warm, professional, and supportive.

# EXPERTISE AREAS
- Indian Penal Code (IPC): Sections 354-376 (assault, harassment, rape), 498A (dowry), 509 (modesty insult)
- Special Acts: POCSO Act 2012, Domestic Violence Act 2005, IT Act 2000, Sexual Harassment at Workplace Act 2013
- Women's health, reproductive rights, and emergency protocols
- Emergency helplines and support networks
- Safety prevention strategies and victim support

# RULES
1. Write naturally and comprehensively like ChatGPT - use flowing paragraphs, not rigid sections
2. Prioritize accuracy - reference database information provided when available
3. Use empathetic, supportive, and professional tone
4. Cite specific legal sections when discussing laws with explanations
5. Include actionable guidance naturally within the response
6. Maintain conversation continuity by referencing previous exchanges
7. Default to Indian legal framework unless specified otherwise

# CONSTRAINTS
- NO medical diagnoses or prescriptions (refer to healthcare professionals)
- NO specific legal advice (suggest consulting lawyers for case-specific situations)
- NO unverified information (distinguish facts from general guidance)
- NO dismissive language or minimization of concerns
- NO marketing or promotional content
- NO structured sections like "Direct Answer", "Action Steps", "Resources" as separate headers

# RESPONSE STYLE
Write long-form, comprehensive responses similar to ChatGPT:
- Use natural flowing paragraphs instead of bullet points when possible
- Break content into logical paragraphs for readability
- Weave in helpline numbers, legal references, and action steps naturally within the narrative
- Provide detailed explanations and context
- End with relevant resources only if they add value
- Aim for 300-500+ words for comprehensive queries, shorter for simple questions"""


# ========== USER PROMPT BUILDER ==========


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
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_threads (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user VARCHAR(255),
                title VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

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
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


ensure_table_exists()


# ----------------- AUTH ENDPOINTS -----------------
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
    except Exception:
        print(f"Register error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Server error"})


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
    except Exception:
        print(f"Login error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Server error"})


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
    except Exception:
        print(f"Forgot password error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Server error"})


# ----------------- HELPER FUNCTIONS -----------------
def get_conversation_history(cursor, chat_id, limit=10):
    """Fetch recent conversation history for context"""
    try:
        cursor.execute(
            "SELECT role, content FROM messages WHERE chat_id = %s ORDER BY timestamp DESC LIMIT %s",
            (chat_id, limit)
        )
        messages = cursor.fetchall()
        return [(msg[0], msg[1]) for msg in reversed(messages)]
    except:
        return []


def build_user_prompt(user_message, contexts, conversation_history):
    """Build clean user prompt with conversation history and knowledge base context"""
    
    prompt_parts = []
    
    # 1. CONVERSATION HISTORY (if exists)
    if conversation_history:
        prompt_parts.append("## Conversation History")
        for role, msg in conversation_history[-5:]:  # Last 5 exchanges
            prefix = "**User**" if role == "user" else "**Assistant**"
            prompt_parts.append(f"{prefix}: {msg}")
        prompt_parts.append("")
    
    # 2. KNOWLEDGE BASE CONTEXT (if exists)
    if contexts:
        prompt_parts.append("## Knowledge Base References")
        for i, ctx in enumerate(contexts, 1):
            metadata = ctx.get('metadata', {})
            source_type = metadata.get('type', 'general').upper()
            section = metadata.get('section', '')
            score = ctx.get('score', 0)
            
            prompt_parts.append(f"**Source {i}** ({source_type} | Relevance: {score:.1%})")
            if section:
                prompt_parts.append(f"Section: {section}")
            prompt_parts.append(f"{ctx.get('text', 'N/A')}")
            prompt_parts.append("")
    else:
        prompt_parts.append("## Knowledge Base References")
        prompt_parts.append("No specific database matches found. Use general expertise.")
        prompt_parts.append("")
    
    # 3. CURRENT QUERY
    prompt_parts.append("## User Query")
    prompt_parts.append(user_message)
    
    return "\n".join(prompt_parts)


# ----------------- CHAT ENDPOINT -----------------
@app.post("/chat")
async def chat(request: Request):
    conn = None
    cursor = None
    try:
        data = await request.json()
        user_msg = data.get("message", "")
        user = data.get("user", "anonymous")
        chat_id = data.get("chat_id")

        if not user_msg:
            return JSONResponse(status_code=400, content={"error": "Message missing"})

        conn = get_connection()
        cursor = conn.cursor()

        # Create new thread if chat_id not provided
        if not chat_id:
            cursor.execute(
                "INSERT INTO chat_threads (user, title) VALUES (%s, %s)",
                (user, user_msg[:50])
            )
            chat_id = cursor.lastrowid
            conn.commit()

        # Insert user message
        cursor.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s)",
            (chat_id, "user", user_msg)
        )
        conn.commit()

        # RAG retrieval
        contexts = []
        try:
            contexts = retrieve_context(user_msg, top_k=5)
        except Exception as rag_error:
            print(f"RAG retrieval failed: {rag_error}")

        # Get conversation history
        conversation_history = get_conversation_history(cursor, chat_id, limit=10)

        # Build user prompt (now separate from system prompt)
        user_prompt = build_user_prompt(user_msg, contexts, conversation_history)

        # LLM call with properly separated system and user prompts
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=user_prompt,  # User prompt only
                config={
                    "system_instruction": SYSTEM_PROMPT,  # System prompt separate
                    "temperature": 0.7,
                    "max_output_tokens": 2000,
                }
            )
            
            bot_reply = response.text
                
        except Exception as gemini_error:
            print(f"Gemini API Error: {gemini_error}")
            print(f"Error type: {type(gemini_error).__name__}")
            print(f"Full traceback: {traceback.format_exc()}")
            
            error_msg = str(gemini_error).lower()
            if "api key" in error_msg or "authentication" in error_msg:
                bot_reply = "API authentication failed. Please check your GEMINI_API_KEY configuration."
            elif "quota" in error_msg or "rate limit" in error_msg:
                bot_reply = "API quota exceeded. Please try again later or check your API usage limits."
            elif "not found" in error_msg or "404" in error_msg:
                bot_reply = f"Model '{GEMINI_MODEL}' not available. Available models: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash"
            else:
                bot_reply = "I'm having trouble connecting to the AI service. Please try again."

        # Insert assistant reply
        cursor.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s)",
            (chat_id, "assistant", bot_reply)
        )
        conn.commit()

        # Prepare sources
        sources = []
        for ctx in contexts[:3]:
            try:
                source = {
                    "text": (ctx.get("text") or "")[:200] + "..." if ctx.get("text") else "N/A",
                    "type": ctx.get("metadata", {}).get("type", "unknown"),
                    "section": ctx.get("metadata", {}).get("section", ""),
                    "relevance": round(ctx.get("score", 0), 3)
                }
                sources.append(source)
            except Exception:
                continue

        return {"reply": bot_reply, "sources": sources, "chat_id": chat_id}

    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"Chat endpoint error ({error_type}): {error_msg}")
        print(f"Full traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500, 
            content={"error": f"Chat service unavailable: {error_type} - {error_msg}"}
        )
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ----------------- CHAT HISTORY MANAGEMENT -----------------
@app.get("/chat_history/{username}")
async def get_chat_history(username: str):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, title, created_at FROM chat_threads WHERE user = %s ORDER BY created_at DESC",
            (username,)
        )
        threads = cursor.fetchall()

        for thread in threads:
            cursor.execute(
                "SELECT role, content, timestamp FROM messages WHERE chat_id = %s ORDER BY timestamp ASC",
                (thread["id"],)
            )
            thread["messages"] = cursor.fetchall()

        return {"chat_history": threads}

    except Exception:
        print(f"Chat history error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Failed to fetch history"})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.delete("/delete_chat/{chat_id}")
async def delete_chat(chat_id: int):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM messages WHERE chat_id = %s", (chat_id,))
        cursor.execute("DELETE FROM chat_threads WHERE id = %s", (chat_id,))
        conn.commit()

        return {"message": "Chat deleted successfully"}

    except Exception:
        print(f"Delete chat error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Delete failed"})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.put("/rename_chat/{chat_id}")
async def rename_chat(chat_id: int, request: Request):
    conn = None
    cursor = None
    try:
        data = await request.json()
        new_title = data.get("title")

        if not new_title:
            return JSONResponse(status_code=400, content={"error": "Title required"})

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE chat_threads SET title = %s WHERE id = %s",
            (new_title, chat_id)
        )
        conn.commit()

        return {"message": "Chat renamed successfully"}

    except Exception:
        print(f"Rename chat error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Rename failed"})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ----------------- GOOGLE AUTH -----------------
@app.get("/auth/google")
async def auth_google():
    return {"auth_url": google_login()}


@app.get("/auth/callback")
async def auth_google_callback(code: str):
    try:
        user_info = google_callback(code)
        success = save_google_user(user_info)
        if success:
            username = user_info["email"]
            display_name = user_info.get("name", username)
            redirect_url = (
                f"http://127.0.0.1:8501/"
                f"?google_login=1&user={urllib.parse.quote(username)}"
                f"&name={urllib.parse.quote(display_name)}"
            )
            return RedirectResponse(redirect_url)
        return JSONResponse(status_code=500, content={"error": "Failed to save Google user"})
    except Exception:
        print(f"Google callback error: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Google login failed"})


@app.get("/verify-google-login")
async def verify_google_login(user: str):
    return {"message": "Login successful", "user": user, "logged_in": True}


# ----------------- UTILITY ENDPOINTS -----------------
@app.get("/list-models")
async def list_models():
    """List all available Gemini models for debugging"""
    try:
        available = []
        for m in client.models.list():
            available.append({
                "name": m.name,
                "display_name": getattr(m, 'display_name', m.name)
            })
        return {
            "current_model": GEMINI_MODEL,
            "available_models": available,
            "total_count": len(available)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to list models: {str(e)}"}
        )


# ----------------- HEALTH CHECK -----------------
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": GEMINI_MODEL,
        "api_configured": bool(GEMINI_API_KEY)
    }


@app.get("/")
async def root():
    return {
        "message": "Women's Safety Chatbot API",
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "list_models": "/list-models",
            "chat": "/chat",
            "register": "/register",
            "login": "/login"
        }
    }


@app.delete("/clear_messages_after/{chat_id}/{message_count}")
async def clear_messages_after(chat_id: int, message_count: int):
    """Clear messages after a specific count (used when editing messages)"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all message IDs for this chat
        cursor.execute(
            "SELECT id FROM messages WHERE chat_id = %s ORDER BY timestamp ASC",
            (chat_id,)
        )
        message_ids = [row[0] for row in cursor.fetchall()]
        
        # Delete messages beyond the specified count
        if len(message_ids) > message_count:
            ids_to_delete = message_ids[message_count:]
            placeholders = ','.join(['%s'] * len(ids_to_delete))
            cursor.execute(f"DELETE FROM messages WHERE id IN ({placeholders})", ids_to_delete)
            conn.commit()
            return {"status": "success", "deleted": len(ids_to_delete)}
        
        return {"status": "success", "deleted": 0}
    except Exception as e:
        print(f"Clear messages error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    import uvicorn
    print(f"Starting server with model: {GEMINI_MODEL}")
    uvicorn.run(app, host="127.0.0.1", port=8000)