import uuid
import asyncio
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from app.service import SearchService


def get_search_service():
    return SearchService()

app = FastAPI()

@app.post("/search")
async def search_flights(search_service: SearchService = Depends(get_search_service)):
    search_id = str(uuid.uuid4())
    asyncio.create_task(search_service.search_async(search_id))
    return {'search_id': search_id}

@app.get("/results/{search_id}/{currency}")
def get_results(search_id: str, currency: str, search_service: SearchService = Depends(get_search_service)):
    if not search_service.is_valid_search_id(search_id):
        return JSONResponse(content={"message": "Invalid search_id"})
    result = search_service.get_results(search_id, currency)
    return JSONResponse(content=result)
