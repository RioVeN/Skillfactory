import telebot
from config import TOKEN, keys, keys_parser
from extensions import CurrencyConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)
dict_keys = {}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \nИмя валюты которую переводим, \
в какую валюту переводим, количество переводимой валюты\n\
Для конвертации с помощью кнопок введите команду /button\n\
Для того чтобы узнать перечень валют доступных для конвертации введите команду /values\n\
Для того чтобы узнать текущий курс введите команду /curs'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['button'])
def button(message: telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    item_1 = telebot.types.InlineKeyboardButton('💵 USD ', callback_data='is.button_USD')
    item_2 = telebot.types.InlineKeyboardButton('💶 EUR', callback_data='is.button_EUR')
    item_3 = telebot.types.InlineKeyboardButton('🇷🇺 RUB', callback_data='is.button_RUB')
    markup.add(item_1, item_2, item_3)
    bot.send_message(message.chat.id, 'Выберите валюту для конвертации', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('is'))
def callback(call):
    if call.data == 'is.button_USD':
        dict_keys['quote'] = 'Доллар'
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        item_2 = telebot.types.InlineKeyboardButton('💶 EUR', callback_data='in.button_in_EUR')
        item_3 = telebot.types.InlineKeyboardButton('🇷🇺 RUB', callback_data='in.button_in_RUB')
        markup.add(item_2, item_3)
        bot.send_message(call.message.chat.id, 'Выберите валюту в которую конвертируем', reply_markup=markup)
    elif call.data == 'is.button_EUR':
        dict_keys['quote'] = 'Евро'
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        item_1 = telebot.types.InlineKeyboardButton('💵 USD ', callback_data='in.button_in_USD')
        item_3 = telebot.types.InlineKeyboardButton('🇷🇺 RUB', callback_data='in.button_in_RUB')
        markup.add(item_1, item_3)
        bot.send_message(call.message.chat.id, 'Выберите валюту в которую конвертируем', reply_markup=markup)
    elif call.data == 'is.button_RUB':
        dict_keys['quote'] = 'Рубль'
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        item_1 = telebot.types.InlineKeyboardButton('💵 USD ', callback_data='in.button_in_USD')
        item_2 = telebot.types.InlineKeyboardButton('💶 EUR', callback_data='in.button_in_EUR')
        markup.add(item_1, item_2)
        bot.send_message(call.message.chat.id, 'Выберите валюту в которую конвертируем', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('in'))
def callback2(call):
    if call.data == 'in.button_in_RUB':
        dict_keys['base'] = 'Рубль'
        bot.send_message(call.message.chat.id, 'Введите сумму')
    if call.data == 'in.button_in_USD':
        dict_keys['base'] = 'Доллар'
        bot.send_message(call.message.chat.id, 'Введите сумму')

    if call.data == 'in.button_in_EUR':
        dict_keys['base'] = 'Евро'
        bot.send_message(call.message.chat.id, 'Введите сумму')


@bot.message_handler(commands=['values'])
def currency(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['curs'])
def curs(message: telebot.types.Message):
    text = 'Текущий курс'
    for key, val in keys_parser.items():
        text = '\n'.join((text, f'{key} = {val} '))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converted1(message: telebot.types.Message):
    values = message.text.title().split()

    if len(values) == 1:
        try:
            amount = message.text
            total_base2 = CurrencyConverter.converter(dict_keys['quote'], dict_keys['base'], amount)
            text = f'Цена {amount} {dict_keys["quote"]} в {dict_keys["base"]} = {str(round(total_base2, 2))}'
            bot.send_message(message.chat.id, text)
        except (ConvertionException, KeyError) as e:
            bot.reply_to(message, f'Ошибка пользователя ')

    elif len(values) != 3:
        try:
            raise ConvertionException('Невозможно обработать запрос, количество аргументов не равно трем!')
        except ConvertionException as e:
            bot.reply_to(message, f'Ошибка пользователя \n {e}')

    elif len(values) == 3:
        try:
            quote, base, amount = values
            total_base = CurrencyConverter.converter(quote, base, amount)
            text = f'Цена {amount} {quote} в {base} = {str(round(total_base, 2))}'
            bot.send_message(message.chat.id, text)
        except ConvertionException as e:
            bot.reply_to(message, f"Ошибка пользователя \n {e}")


bot.polling()
