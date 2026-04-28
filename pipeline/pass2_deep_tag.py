import asyncio, aiofiles
from pipeline.config import supabase, SEM
from pipeline.utils.llm_clients import gemini_pro
from pipeline.utils.prompts import DEEP_TAG_PROMPT

async def tag(row):
    async with SEM:
        try:
            async with aiofiles.open(row["path"], "rb") as f:
                d = await gemini_pro(DEEP_TAG_PROMPT, await f.read())
            supabase.table("photos").update({
                "dish": d.get("dish"), "cuisine": d.get("cuisine"),
                "category": d.get("category"), "ingredients": d.get("ingredients"),
                "cooking_method": d.get("cooking_method"),
                "plating_context": d.get("plating_context"),
                "confidence": d.get("confidence"),
            }).eq("id", row["id"]).execute()
        except Exception as e:
            print("deep_tag err", row["path"], e)

async def main():
    rows = supabase.table("photos").select("id,path").eq("is_food", True).is_("dish", "null").execute().data
    print(f"deep tagging {len(rows)} food photos")
    await asyncio.gather(*(tag(r) for r in rows))

if __name__ == "__main__":
    asyncio.run(main())