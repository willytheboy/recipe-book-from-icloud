import asyncio, aiofiles
from pipeline.config import supabase, SEM
from pipeline.utils.llm_clients import gemini_flash
from pipeline.utils.prompts import TRIAGE_PROMPT

async def triage(row):
    async with SEM:
        try:
            async with aiofiles.open(row["path"], "rb") as f:
                data = await gemini_flash(TRIAGE_PROMPT, await f.read())
            supabase.table("photos").update({
                "is_food": data["is_food"],
                "coarse_category": data.get("coarse_category"),
            }).eq("id", row["id"]).execute()
        except Exception as e:
            print("triage err", row["path"], e)

async def main():
    rows = supabase.table("photos").select("id,path").is_("is_food","null").limit(100000).execute().data
    await asyncio.gather(*(triage(r) for r in rows))

if __name__ == "__main__":
    asyncio.run(main())
