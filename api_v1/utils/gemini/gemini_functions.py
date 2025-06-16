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
    for i in range(len(response)):
        if 'embedding' in response[i]: del response[i]['embedding']
    return response

def recall_information(data: RecallInformation):
    response = supabase.vector_similarity("match_user_memory", data.embedding, data.top_k)
    if not response:
        raise ValueError("Failed to recall information.")
    for i in range(len(response.data)):
        if 'embedding' in response.data[i]: del response.data[i]['embedding']
    return response