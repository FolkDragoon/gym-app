from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    # Just test the connection
    try:
        supabase.table("members").select("id").limit(1).execute()
        print("Connected to Supabase successfully.")
    except Exception as e:
        print(f"Supabase connection failed: {e}")