import json
import telebot
import requests


TOKEN = '7727321887:AAFm9uihnjVWyqnpABIu4EKmKxOwF_oqWkE'


bot = telebot.TeleBot(TOKEN)

keys = {
    'TON': 'TON',
    'NOT': 'NOT',
    'RUB': 'RUB',
    'BTC': 'BTC',
    'USD': 'USD',
    'тонкоин': 'TON',
    'рубль': 'RUB',
    'доллар': 'USD',
    'биткоин': 'BTC'
}


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def converter(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать {quote} в {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось конвертировать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось конвертировать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось конвертировать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base


# @bot.message_handler()
# def test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'Привет. Команды /start или /help для справки по использованию бота')


@bot.message_handler(commands=['start', 'help'])
def command_help(message: telebot.types.Message):
    text = ('Для начала работы с ботом введите команду формата: <имя валюты> <в какую валюту перевести> <количество>\n'
            'Например: доллар тонкоин 100\n'
            'Увидеть список доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    count_values = message.text.split(' ')

    if len(count_values) != 3:
        raise ConvertionException('Требуются ровно 3 параметра')

    quote, base, amount = count_values
    total_base = CryptoConverter.converter(quote, base, amount)
    if quote == 'RUB' or 'рубль':
        text = f'Цена {amount} {quote} в {base} равна {float(total_base) * float(amount)} {base}'
        bot.send_message(message.chat.id, text)
    else:
        text = f'Цена {amount} {quote} в {base} равна {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
