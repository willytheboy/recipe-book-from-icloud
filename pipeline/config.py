import os, asyncio
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE"])
SEM = asyncio.Semaphore(int(os.environ.get("CONCURRENCY", 8)))