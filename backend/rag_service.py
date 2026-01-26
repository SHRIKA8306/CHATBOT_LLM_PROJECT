"""
RAG Service for Women's Safety Chatbot
Handles vector search and context retrieval from Chroma DB
"""
import json
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CONFIGURATION
# ============================================
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "women_safety_data")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================
# INITIALIZE SERVICES (Lazy loading)
# ============================================
_chroma_client = None
_collection = None
_embedder = None

def get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    return _chroma_client

def get_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        try:
            _collection = client.get_collection(name=COLLECTION_NAME)
        except:
            # Collection doesn't exist, create it
            _collection = client.create_collection(name=COLLECTION_NAME)
    return _collection

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
    return _embedder

# ============================================
# DATA PROCESSING FUNCTIONS
# ============================================
def process_helplines(helplines_data):
    """Convert helplines JSON to searchable chunks"""
    chunks = []
    
    # National helplines
    for helpline in helplines_data.get("national_helplines_all_india", []):
        chunk_text = f"National Helpline: {helpline['description']}. "
        chunk_text += f"Numbers: {', '.join(helpline['number'])}. "
        chunk_text += f"Available: {helpline['timings']}"
        
        chunks.append({
            "id": f"national_{len(chunks)}",
            "text": chunk_text,
            "metadata": {
                "type": "national_helpline",
                "numbers": ", ".join(helpline["number"]),
                "description": helpline["description"],
                "timings": helpline["timings"]
            }
        })
    
    # State-wise helplines
    for state_data in helplines_data.get("state_wise_women_helplines", []):
        state = state_data["state"]
        for helpline in state_data["helplines"]:
            chunk_text = f"{state} Helpline: {helpline['description']}. "
            chunk_text += f"Numbers: {', '.join(helpline['number'])}. "
            chunk_text += f"Timings: {helpline['timings']}"
            
            chunks.append({
                "id": f"state_{state.replace(' ', '_')}_{len(chunks)}",
                "text": chunk_text,
                "metadata": {
                    "type": "state_helpline",
                    "state": state,
                    "numbers": ", ".join(helpline["number"]),
                    "description": helpline["description"],
                    "timings": helpline["timings"]
                }
            })
    
    # NGO helplines
    for ngo in helplines_data.get("organizations_and_ngo_providing_free_guidance_and_support", []):
        chunk_text = f"NGO Support: {ngo['description']}. "
        chunk_text += f"Numbers: {', '.join(ngo['number'])}. "
        chunk_text += f"Timings: {ngo['timings']}"
        
        chunks.append({
            "id": f"ngo_{len(chunks)}",
            "text": chunk_text,
            "metadata": {
                "type": "ngo",
                "numbers": ", ".join(ngo["number"]),
                "description": ngo["description"],
                "timings": ngo["timings"]
            }
        })
    
    return chunks

def process_laws(laws_data):
    """Convert laws JSON to searchable chunks with better structure"""
    chunks = []
    
    for section_key, section_data in laws_data.items():
        # Create multiple chunks per law for better retrieval:
        # 1. Full law chunk
        full_chunk_text = f"{section_key}: {section_data['main_keywords']}. "
        full_chunk_text += f"Details: {section_data['info']} "
        full_chunk_text += f"Punishment: {section_data['punishment']}"
        
        chunks.append({
            "id": f"law_full_{section_key.replace(' ', '_').replace('/', '_')}",
            "text": full_chunk_text,
            "metadata": {
                "type": "legal",
                "section": section_key,
                "keywords": section_data["main_keywords"],
                "info": section_data["info"],
                "punishment": section_data["punishment"]
            }
        })
        
        # 2. Keywords-focused chunk for better keyword matching
        keyword_chunk = f"{section_key} related to {section_data['main_keywords']}. This law covers: {section_data['info']}"
        chunks.append({
            "id": f"law_keywords_{section_key.replace(' ', '_').replace('/', '_')}",
            "text": keyword_chunk,
            "metadata": {
                "type": "legal_keywords",
                "section": section_key,
                "keywords": section_data["main_keywords"],
                "info": section_data["info"],
                "punishment": section_data["punishment"]
            }
        })
    
    return chunks

def upload_to_chroma(chunks, batch_size=100):
    """Generate embeddings and upload to Chroma DB"""
    collection = get_collection()
    embedder = get_embedder()

    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for chunk in chunks:
        embedding = embedder.encode(chunk["text"]).tolist()

        ids.append(chunk["id"])
        embeddings.append(embedding)
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])

        if len(ids) >= batch_size:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            print(f"Uploaded {len(ids)} vectors to Chroma DB")
            ids, embeddings, metadatas, documents = [], [], [], []

    if ids:
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        print(f"Uploaded {len(ids)} vectors to Chroma DB")

# ============================================
# SETUP FUNCTION (Run once)
# ============================================
def setup_rag():
    """Load data and upload to Chroma DB - RUN THIS ONCE"""
    with open("data/helplines.json", "r", encoding="utf-8") as f:
        helplines_data = json.load(f)

    with open("data/laws.json", "r", encoding="utf-8") as f:
        laws_data = json.load(f)

    helpline_chunks = process_helplines(helplines_data)
    law_chunks = process_laws(laws_data)
    all_chunks = helpline_chunks + law_chunks

    upload_to_chroma(all_chunks)
    print(f"✅ Successfully uploaded {len(all_chunks)} chunks to Chroma DB!")

# ============================================
# RETRIEVAL FUNCTIONS
# ============================================
def retrieve_context(query, top_k=5):
    """Retrieve relevant context from Chroma DB"""
    collection = get_collection()
    embedder = get_embedder()

    query_embedding = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['metadatas', 'documents', 'distances']
    )

    contexts = []
    if results['documents'] and results['metadatas'] and results['distances']:
        for i in range(len(results['documents'][0])):
            contexts.append({
                "text": results['documents'][0][i],
                "score": 1 - results['distances'][0][i],  # Convert distance to similarity score
                "metadata": results['metadatas'][0][i]
            })

    return contexts

def build_rag_prompt(user_message, contexts):
    """Build enhanced prompt with retrieved context and better instructions
    (Kept for backward compatibility - use build_conversation_with_rag instead)"""
    
    if contexts:
        context_str = "\n\n".join([f"**Relevant Information {i+1}:**\n{ctx['text']}" 
                                   for i, ctx in enumerate(contexts)])
    else:
        context_str = "No specific information found in database."
    
    prompt = f"""You are a knowledgeable Women's Safety Assistant with expertise in Indian laws, women's rights, and safety resources.

RETRIEVED VERIFIED INFORMATION:
{context_str}

INSTRUCTIONS:
1. **Answer women's safety questions comprehensively** - Even if context is limited, provide your knowledge about relevant laws, protections, and resources
2. **Use retrieved information** when available and mark it clearly (e.g., "According to Section XYZ..." or "Per the helpline database...")
3. **Include relevant details** like:
   - Specific law sections or acts that apply
   - Punishments for violations (if asking about crimes)
   - Relevant helpline numbers from your knowledge
   - Available protections and legal remedies
4. **For out-of-scope questions** (unrelated to women's safety), politely decline
5. **Always prioritize safety** - For emergencies, always recommend calling 112 (emergency) or 100 (police)
6. **Be empathetic and supportive** - Use clear, simple language
7. **Provide actionable information** - Help the user understand their options and next steps

User Question: {user_message}

Your Response:"""
    
    return prompt

# ============================================
# MAIN TESTING
# ============================================
if __name__ == "__main__":
    # Uncomment to upload data to Chroma DB (run once)
    setup_rag()

    # Test retrieval
    test_query = "What helplines are available in Kerala for domestic violence?"
    contexts = retrieve_context(test_query, top_k=3)

    print("Query:", test_query)
    print("\nRetrieved Contexts:")
    for i, ctx in enumerate(contexts, 1):
        print(f"\n{i}. Score: {ctx['score']:.3f}")
        print(f"   {ctx['text'][:200]}...")

    print("\n" + "="*50)
    print("\nEnhanced Prompt:")
    print(build_rag_prompt(test_query, contexts))