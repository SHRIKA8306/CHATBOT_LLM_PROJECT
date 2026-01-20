import json
import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CONFIGURATION
# ============================================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")
PINECONE_CLOUD = "aws"
PINECONE_REGION = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================
# INITIALIZE SERVICES (Lazy loading)
# ============================================
_pc = None
_index = None
_embedder = None

def get_pinecone_client():
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
    return _pc

def get_index():
    global _index
    if _index is None:
        pc = get_pinecone_client()
        if PINECONE_INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)
            )
        _index = pc.Index(PINECONE_INDEX_NAME)
    return _index

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
                "numbers": helpline["number"],
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
                    "numbers": helpline["number"],
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
                "numbers": ngo["number"],
                "description": ngo["description"],
                "timings": ngo["timings"]
            }
        })
    
    return chunks

def process_laws(laws_data):
    """Convert laws JSON to searchable chunks"""
    chunks = []
    
    for section_key, section_data in laws_data.items():
        chunk_text = f"{section_key}: {section_data['main_keywords']}. "
        chunk_text += f"Details: {section_data['info']} "
        chunk_text += f"Punishment: {section_data['punishment']}"
        
        chunks.append({
            "id": f"law_{section_key.replace(' ', '_').replace('/', '_')}",
            "text": chunk_text,
            "metadata": {
                "type": "legal",
                "section": section_key,
                "keywords": section_data["main_keywords"],
                "info": section_data["info"],
                "punishment": section_data["punishment"]
            }
        })
    
    return chunks

def upload_to_pinecone(chunks, batch_size=100):
    """Generate embeddings and upload to Pinecone"""
    index = get_index()
    embedder = get_embedder()
    vectors = []
    
    for chunk in chunks:
        embedding = embedder.encode(chunk["text"]).tolist()
        
        vectors.append({
            "id": chunk["id"],
            "values": embedding,
            "metadata": {
                "text": chunk["text"],
                **chunk["metadata"]
            }
        })
        
        if len(vectors) >= batch_size:
            index.upsert(vectors=vectors)
            print(f"Uploaded {len(vectors)} vectors")
            vectors = []
    
    if vectors:
        index.upsert(vectors=vectors)
        print(f"Uploaded {len(vectors)} vectors")

# ============================================
# SETUP FUNCTION (Run once)
# ============================================
def setup_rag():
    """Load data and upload to Pinecone - RUN THIS ONCE"""
    with open("data/helplines.json", "r", encoding="utf-8") as f:
        helplines_data = json.load(f)
    
    with open("data/laws.json", "r", encoding="utf-8") as f:
        laws_data = json.load(f)
    
    helpline_chunks = process_helplines(helplines_data)
    law_chunks = process_laws(laws_data)
    all_chunks = helpline_chunks + law_chunks
    
    upload_to_pinecone(all_chunks)
    print(f"✅ Successfully uploaded {len(all_chunks)} chunks to Pinecone!")

# ============================================
# RETRIEVAL FUNCTIONS
# ============================================
def retrieve_context(query, top_k=3):
    """Retrieve relevant context from Pinecone"""
    index = get_index()
    embedder = get_embedder()
    
    query_embedding = embedder.encode(query).tolist()
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    contexts = []
    for match in results['matches']:
        contexts.append({
            "text": match['metadata']['text'],
            "score": match['score'],
            "metadata": match['metadata']
        })
    
    return contexts

def build_rag_prompt(user_message, contexts):
    """Build enhanced prompt with retrieved context"""
    context_str = "\n\n".join([f"Context {i+1}: {ctx['text']}" 
                               for i, ctx in enumerate(contexts)])
    
    prompt = f"""You are a Women's Safety Assistant with access to verified information about helplines and laws in India.

VERIFIED INFORMATION:
{context_str}

INSTRUCTIONS:
- ONLY answer questions related to women's safety in India
- Use the VERIFIED INFORMATION above when relevant
- Include specific helpline numbers and law sections from the context
- If the question is unrelated to women's safety, politely say: "Sorry, I can only answer questions about women's safety."
- Be empathetic, clear, and supportive
- Always prioritize immediate safety (suggest calling 112 or 100 for emergencies)

User Question: {user_message}

Your Response:"""
    
    return prompt

# ============================================
# MAIN TESTING
# ============================================
if __name__ == "__main__":
    # Uncomment to upload data to Pinecone (run once)
    #setup_rag()