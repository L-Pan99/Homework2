import requests
import json
from config import keys

class APIException(Exception):

    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Нельзя переводить одинаковые валюты {base}.')

        if quote not in keys:
            raise APIException(f'Не удалось обработать валюту {quote}')
        if base not in keys:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        quote_ticker = keys[quote]
        base_ticker = keys[base]

        url = f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}'
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException('Ошибка запроса к API. Попробуйте позже.')

        try:
            rate = json.loads(response.content)[base_ticker]
        except KeyError:
            raise APIException('Ошибка обработки ответа от API.')

        total_base = round(rate * amount, 2)
        return total_base