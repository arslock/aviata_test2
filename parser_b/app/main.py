import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.service import get_flights

app = FastAPI()


@app.get("/search")
def search_flights():
    time.sleep(60)
    return JSONResponse(get_flights())
