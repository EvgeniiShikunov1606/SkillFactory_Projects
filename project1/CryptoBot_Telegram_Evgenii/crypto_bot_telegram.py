import random
import telebot
from extensions import APIException, CryptoConverter
from config import keys, TOKEN, commands_list

# link to bot - @evgenii_crypto_bot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    text = ('Бот "CryptoBot_Evgenii" помогает конвертировать валюты.\n'
            'Помощь по руководству доступна командой: /help\n'
            'Список доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    value_1, value_2 = random.sample(list(keys.keys()), 2)
    text = ('Для начала работы с ботом введите команду формата:\n <имя валюты> <в какую валюту перевести> <количество>'
            f'\nНапример: {value_1} {value_2} {random.randint(1, 100)}\n'
            'Использовать только аббревиатуры.\n'
            'Узнать список доступных валют: /values\n'
            'Список доступных команд: /com')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['com'])
def com(message: telebot.types.Message):
    text = 'Доступные команды:'
    for i in commands_list:
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        start_values = message.text
        if start_values.startswith('/'):
            if start_values not in commands_list:
                available_commands = [str(command) for command in commands_list]
                raise APIException(f'Команда {start_values} недоступна.\n'
                                          f'Список доступных команд: {', '.join(available_commands)}')
        count_values = message.text.split()
        if len(count_values) > 3:
            count_values = count_values[:3]
        elif len(count_values) < 3:
            raise APIException(f'Некорректное кол-во параметров (требуются 3). У вас их {len(count_values)}')

        quote, base, amount = count_values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = (f'Цена {amount} {str(quote).upper()} в {str(base).upper()} '
                f'равна {float(total_base) * float(amount)} {str(base).upper()}')
        bot.send_message(message.chat.id, text)


bot.polling()

