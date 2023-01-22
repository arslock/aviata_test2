import asyncio
import uuid
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from app.service import send_request_to_providers, get_search_results, create_currencies_json_file, \
    add_price, providers

app = FastAPI()


@app.post("/search")
async def search_flights():
    search_id = str(uuid.uuid4())
    asyncio.create_task(send_request_to_providers(search_id))
    return {'search_id': search_id}


@app.get("/result/{search_id}/{currency}")
def get_results(search_id: str, currency: str):
    result = get_search_results(search_id, currency)
    return JSONResponse(result)


# currency_json = get_currencies()
#
# create_currencies_json_file(currency_json)

# add_price(1, 'KZT')

# print('AAAAAAAAA')
# test_request_to_services()

