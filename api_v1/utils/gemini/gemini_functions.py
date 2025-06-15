from datetime import datetime
from api_v1.utils.supabase_db.supabase_main import SupabaseDB
from core.models.database_model import Memory
from core.models.gemini_functions_models import MemorizeInformation, RecallInformation

supabase = SupabaseDB()



def memorize_information(data : MemorizeInformation):
    
    memory = Memory(
        content=data.info,
        memory_type=data.memory_type,
        source=data.source,
        confidence=data.confidence,
        tags=data.tags or [],
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        embedding=data.embedding if data.embedding else None
    )

    response = supabase.insert('User_Memory', memory.model_dump(mode='json'))
    return f"Memory {response} has been stored in database."
"""
Hey, do you remember what I preferred to be called as?

And how would you spell it in hiragana? :D
"""

def recall_information(data: RecallInformation):
    response = supabase.vector_similarity("match_user_memory", data.embedding, data.top_k)
    if not response:
        raise ValueError("Failed to recall information.")
    if 'embedding' in response.data[0]: del response.data[0]['embedding']
    return response