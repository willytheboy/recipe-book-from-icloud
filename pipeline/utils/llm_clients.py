import os, json, asyncio
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

async def gemini_flash(prompt, image_bytes):
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = await asyncio.to_thread(model.generate_content,
        [prompt, {"mime_type":"image/jpeg","data":image_bytes}],
        generation_config={"response_mime_type":"application/json"})
    return json.loads(resp.text)

async def gemini_pro(prompt, image_bytes):
    model = genai.GenerativeModel("gemini-2.5-pro")
    resp = await asyncio.to_thread(model.generate_content,
        [prompt, {"mime_type":"image/jpeg","data":image_bytes}],
        generation_config={"response_mime_type":"application/json"})
    return json.loads(resp.text)
