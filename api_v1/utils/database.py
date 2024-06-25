from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def init_db():
    supabase : Client = create_client(os.getenv("SUPA_API_URL"),os.getenv("SUPA_API_KEY"))
    return supabase