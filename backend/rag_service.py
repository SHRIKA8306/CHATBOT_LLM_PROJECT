"""
RAG Service for Women's Safety Chatbot
Handles vector search and context retrieval from Pinecone
"""
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
def retrieve_context(query, top_k=5):
    """Retrieve relevant context from Pinecone with multi-query strategy"""
    index = get_index()
    embedder = get_embedder()
    
    # Collect results from original query
    all_results = {}
    
    query_embedding = embedder.encode(query).tolist()
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    for match in results['matches']:
        match_id = match['id']
        all_results[match_id] = {
            "text": match['metadata']['text'],
            "score": match['score'],
            "metadata": match['metadata']
        }
    
    # Sort by score and return top results
    sorted_results = sorted(all_results.values(), key=lambda x: x['score'], reverse=True)
    
    contexts = []
    for result in sorted_results[:top_k]:
        contexts.append(result)
    
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
    # Uncomment to upload data to Pinecone (run once)
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