import os, asyncio
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE"])
SEM = asyncio.Semaphore(int(os.environ.get("CONCURRENCY", 8)))
