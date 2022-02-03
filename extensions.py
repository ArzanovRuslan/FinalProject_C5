import requests
import json
from config import exchanges

class APIException(Exception):                  # создадим класс наследник от Exception
    pass

class Convertor:
    @staticmethod
    def get_price(base, sym, amount):                           # создаем функцию конвертирования
        try:                                                    # создаем конструкцию для отлавливания исключений
            base_key = exchanges[base.lower()]                      # записываем base (валюта) в нижнем регистре из словаря exchanges
        except KeyError:                                        # перехватываем исключение если в словаре exchanges нет такой записи (валюты)
            raise APIException(f"Валюта {base} не найдена!")        # и вызываем исключение класса APIException с сообщением об ошибке

        try:                                                    # создаем конструкцию для отлавливания исключений
            sym_key = exchanges[sym.lower()]                        # записываем sym (валюта) в нижнем регистре из словаря exchanges
        except KeyError:                                        # перехватываем исключение если в словаре exchanges нет такой записи (валюты)
            raise APIException(f"Валюта {sym} не найдена!")         # и вызываем исключение класса APIException с сообщением об ошибке

        if base_key == sym_key:                                                     # проверяем переводимые валюты на повторяемость
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')       # если одинаковые вызываем исключение с сообщением об ошибке

        try:                                                                    # создаем конструкцию для отлавливания исключений
            amount = float(amount.replace(',', '.'))                                # записываем amount приведенную к float и с . если указана ,
        except ValueError:                                                      # перехватываем исключение если amount нельзя привести к float
            raise APIException(f'Не удалось обработать количество {amount}!')       # и вызываем исключение класса APIException с сообщением об ошибке


        # запрашиваем данные с API cryptocompare.com: курс валюты 'tsyms' относительно валюты 'fsym'
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={exchanges[base]}&tsyms={exchanges[sym]}')
        resp = json.loads(r.content)                        # парсим полученные данные в обьект
        new_price = resp[exchanges[sym]] * float(amount)    # сохраняем в переменную количество получившейся валюты
        return round(new_price, 2)       # возвращаем кол-во получившейся валюты с округлением до 2 знаков после запятой