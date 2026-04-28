import os, hashlib, asyncio, aiofiles
from PIL import Image
from pipeline.config import supabase

ROOT = os.environ["LOCAL_PHOTOS_DIR"]

async def hash_file(path):
    h = hashlib.sha256()
    async with aiofiles.open(path, "rb") as f:
        while True:
            chunk = await f.read(1<<20)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()

async def main():
    rows = []
    for dp, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.lower().endswith((".jpg",".jpeg",".png",".heic")): continue
            p = os.path.join(dp, fn)
            try: w,h = Image.open(p).size
            except Exception: continue
            rows.append({"path": p, "sha256": await hash_file(p), "width": w, "height": h})
            if len(rows) >= 500:
                supabase.table("photos").upsert(rows, on_conflict="sha256").execute(); rows=[]
    if rows:
        supabase.table("photos").upsert(rows, on_conflict="sha256").execute()

if __name__ == "__main__":
    asyncio.run(main())
