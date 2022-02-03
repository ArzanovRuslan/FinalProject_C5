import telebot
import traceback
from extensions import Convertor, APIException
from config import *


bot = telebot.TeleBot(TOKEN)    # создаем обьект класса telebot и передаем TOKEN в конструктор класса

@bot.message_handler(commands=['start', 'help'])    # создаем декоратор функции start для отлавливания команд /start и /help
def start(message: telebot.types.Message):          # создаем функцию обработки команд start и help
    text = "Приветствие!"                               # записываем текст ответа в переменную
    bot.send_message(message.chat.id, text)             # передаем текст ответа в чат

@bot.message_handler(commands=['values'])       # создаем декоратор функции values для отлавливания команды /values
def values(message: telebot.types.Message):     # создаем функцию обработки команды /values
    text = 'Доступные валюты:'                      # записываем текст ответа в переменную
    for i in exchanges.keys():                      # создаем цикл для чтения ключей (названия валют) из словаря exchanges
        text = '\n'.join((text, i))                 # добавляем в переменную text ключи из словаря, с переносом на новую строку
    bot.reply_to(message, text)                     # отвечаем на сообщение передачей содержимого переменной text в чат

@bot.message_handler(content_types=['text'])        # создаем декоратор функции converter для обработки любого введенного текста
def converter(message: telebot.types.Message):      # создаем функцию обработки сообщений
    values = message.text.split()           # записываем в values список из полученных данных
    try:                                                            # создаем конструкцию для отлавливания исключений
        if len(values) != 3:                                            # и проверяем количество записей в списке values
            raise APIException('Неверное количество параметров!')           # если оно не равно 3 вызываем исключение
        new_price = Convertor.get_price(*values)                        # передаем параметры и сохраняем возвращенное значение из функции Convertor
    except APIException as e:                                       # перехватываем исключение класса APIException
        bot.reply_to(message, f"Ошибка в команде:\n{e}")                # и отвечаем сообщением в чат месенджера об ошибке
    except Exception as e:                                          # перехватываем исключение Exception
        traceback.print_tb(e.__traceback__)                             # печатаем трассировку исключения
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")              # и отвечаем сообщением в чат месенджера об ошибке
    else:                                                                                       # если исключения не было
        bot.reply_to(message, f"За {values[2]} {values[0]} получим: {new_price} {values[1]} ")  # то отвечаем на сообщение в мессенджере о количестве переведенной валюты


bot.polling()   # опрос бота
