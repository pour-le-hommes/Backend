from datetime import datetime
from typing import List

from litellm import embedding
from api_v1.utils.supabase_db.supabase_main import SupabaseDB
from core.models.database_model import Memory

supabase = SupabaseDB()

def generate_vector_embedding(text: str):
    response = embedding(
        model="gemini/text-embedding-004",
        input=[text],
    )
    embedding_data = response['data'][0]['embedding'] # type: ignore
    return embedding_data

def memorize_information(info:str, memory_type:str='fact', source:str='user', confidence:float=0.0, tags:List[str]=[]):
    embedding_data = generate_vector_embedding(info)
    
    memory = Memory(
        content=info,
        memory_type=memory_type,
        source=source,
        confidence=confidence,
        tags=tags or [],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        embedding= embedding_data if embedding_data else None
    )

    response = supabase.insert('User_Memory', memory.model_dump(mode='json'))
    for i in range(len(response)):
        if 'embedding' in response[i]: del response[i]['embedding']
    return response

def recall_information(info:str, top_k:int):
    embedding_data = generate_vector_embedding(info)
    
    response = supabase.vector_similarity("match_user_memory", embedding_data, top_k)
    if not response:
        raise ValueError("Failed to recall information.")
    for i in range(len(response.data)):
        if 'embedding' in response.data[i]: del response.data[i]['embedding']
    return response