import asyncio, os
from anthropic import AsyncAnthropic
from pipeline.config import supabase
from pipeline.utils.prompts import RECIPE_PROMPT
client = AsyncAnthropic()

async def write_recipe(c):
    photos = supabase.table("photos").select("ingredients").eq("cluster_id", c["id"]).execute().data
    ing = sorted({i for p in photos if p.get("ingredients") for i in p["ingredients"]})
    prompt = RECIPE_PROMPT.format(label=c["label"], cuisine=c.get("cuisine"), category=c.get("category"), n=c["size"], ingredients=", ".join(ing))
    msg = await client.messages.create(model="claude-sonnet-4-5", max_tokens=1500, messages=[{"role":"user","content":prompt}])
    md = msg.content[0].text
    supabase.table("recipes").upsert({
        "cluster_id": c["id"], "title": c["label"],
        "ingredients_md": md, "steps_md": "", "notes_md": "",
        "generated_by": "claude-sonnet-4-5",
    }).execute()

async def main():
    cs = supabase.table("clusters").select("*").execute().data
    print(f"writing recipes for {len(cs)} clusters")
    await asyncio.gather(*(write_recipe(c) for c in cs))

if __name__ == "__main__":
    asyncio.run(main())