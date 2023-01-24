import os
import asyncio
import json
from typing import Dict

import aiohttp
import redis
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
LOCAL_IP = os.environ.get('LOCAL_IP')


class SearchService:
    def __init__(self):
        self.r = redis.Redis(
            host='redis',
            port=6379,
            db=0,
            charset='utf-8',
            decode_responses=True
        )
        self.providers = [
            f"http://{LOCAL_IP}:9001",
            f"http://{LOCAL_IP}:9002"
        ]

    async def request_to_provider(self, provider, search_id) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{provider}/search') as response:
                result = await response.json()
                json_data = self.r.get(search_id)
                data = json.loads(json_data)
                data['items'] += result
                data['count'] += 1

                if data['count'] == 2:
                    data['status'] = 'Completed'

                self.r.set(search_id, json.dumps(data))

    async def search_async(self, search_id: str) -> None:
        data = {'search_id': f'{search_id}', 'status': 'Pending', 'items': [], 'count': 0}
        json_data = json.dumps(data)
        self.r.set(search_id, json_data)

        asyncio.create_task(
            asyncio.gather(*[self.request_to_provider(provider, search_id) for provider in self.providers]))

    def is_valid_search_id(self, search_id: str) -> bool:
        return self.r.get(search_id) is not None

    def get_results(self, search_id: str, currency: str) -> Dict:
        result = self.r.get(search_id)
        json_data = json.loads(result)

        self.filter_by_currency(json_data, currency)
        self.add_price(json_data['items'], currency)
        json_data.pop('count')
        return json_data

    @staticmethod
    def filter_by_currency(data: Dict, currency: str) -> Dict:
        data['items'] = [provider for provider in data['items'] if provider['pricing']['currency'] == currency]
        data['items'] = sorted(data['items'], key=lambda x: x['pricing']['total'], reverse=True)
        return data

    @staticmethod
    def add_price(data: Dict, currency: str) -> Dict:
        with open('app/data/currency_json.json', 'r') as f:
            currency_json = json.load(f)

        exchange_rate = currency_json[currency] if currency != 'KZT' else 1

        for provider in data:
            amount = float(provider['pricing']['total']) * float(exchange_rate)
            provider['price'] = {
                'amount': round(amount, 2),
                'currency': 'KZT'
            }
        return data


def get_currencies() -> json:
    current_date = datetime.today().strftime('%d.%m.%Y')
    url = f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={current_date}'
    response = requests.get(url)
    response_xml = ET.fromstring(response.text)
    items = response_xml.findall('item')
    currencies = {}
    for item in items:
        currencies[f"{item.find('title').text}"] = item.find('description').text

    currency_json = json.dumps(currencies)
    return currency_json


def create_currencies_json_file(currency_json: json) -> None:
    with open('app/data/currency_json.json', 'w') as f:
        f.write(currency_json)