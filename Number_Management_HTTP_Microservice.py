
from fastapi import FastAPI, HTTPException, Query
import httpx
import asyncio

app = FastAPI()

async def fetch_numbers(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                return data.get("numbers", [])
    except asyncio.TimeoutError:
        pass
    return []

@app.get("/numbers")
async def get_numbers(urls: list[str] = Query(..., description="List of URLs")):
    loop = asyncio.get_event_loop()
    tasks = [fetch_numbers(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    unique_numbers = set()
    for num_list in results:
        unique_numbers.update(num_list)
    
    merged_numbers = sorted(unique_numbers)
    
    return {"numbers": merged_numbers}
