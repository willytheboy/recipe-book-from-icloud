import asyncio, aiofiles, os
import google.generativeai as genai
from pipeline.config import supabase, SEM
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

async def embed_one(row):
    async with SEM:
        try:
            async with aiofiles.open(row["path"], "rb") as f:
                data = await f.read()
            emb = await asyncio.to_thread(
                genai.embed_content,
                model="models/embedding-001",
                content={"mime_type": "image/jpeg", "data": data},
                task_type="retrieval_document",
            )
            vec = emb["embedding"]
            if len(vec) > 1024: vec = vec[:1024]
            supabase.table("photos").update({"visual_embedding": vec}).eq("id", row["id"]).execute()
        except Exception as e:
            print("embed err", row["path"], e)

async def main():
    rows = supabase.table("photos").select("id,path").eq("is_food", True).is_("visual_embedding", "null").execute().data
    print(f"embedding {len(rows)} food photos")
    await asyncio.gather(*(embed_one(r) for r in rows))

if __name__ == "__main__":
    asyncio.run(main())