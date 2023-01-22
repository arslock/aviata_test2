from app.service import get_currencies, create_currencies_json_file


def update_currencies():
    data = get_currencies()
    create_currencies_json_file(data)


update_currencies()
