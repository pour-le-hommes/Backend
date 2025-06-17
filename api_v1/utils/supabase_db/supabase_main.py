from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

class SupabaseDB:
    _instance = None
    _client: Client

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseDB, cls).__new__(cls)
            url = os.getenv("SUPABASE_API_URL", "")
            key = os.getenv("SUPABASE_API_KEY", "")
            cls._client: Client = create_client(url, key)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            if not self._client:
                raise ValueError("Supabase client is not initialized. Check your environment variables.")
            pass

    def select(self, table_name: str, *args, **kwargs):
        response = self._client.table(table_name).select(*args, **kwargs).execute()
        return response.data if response.data else []

    def insert(self, table_name: str, data: dict):
        response = self._client.table(table_name).insert(data).execute()
        return response.data if response.data else []

    def update(self, table_name: str, data: dict, match: dict):
        response = self._client.table(table_name).update(data).match(match).execute()
        return response.data if response.data else []

    def delete(self, table_name: str, match: dict):
        response = self._client.table(table_name).delete().match(match).execute()
        return response.data if response.data else []
    
    def vector_similarity(self, function_name, vector_data, match_count):
        response = self._client.rpc(
            function_name,
            {"query_embedding": vector_data, "match_count": match_count}
        ).execute()
        return response

