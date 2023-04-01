from config import keys, keys_parser


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def converter(quote, base, amount):
        if quote == base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {quote}')

        total_base = float(keys_parser[f'{quote_ticker}/{base_ticker}']) * int(amount)
        return total_base
