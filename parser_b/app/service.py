import json


def get_flights():
    try:
        with open('app/data/response_b.json') as f:
            return json.load(f)
    except IOError:
        return None
