import telebot
from extensions import ConvertionException, CryptoConverter
from config import keys, TOKEN, commands_list


bot = telebot.TeleBot(TOKEN)


# @bot.message_handler()
# def test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'Привет. Команды /start или /help для справки по использованию бота')


@bot.message_handler(commands=['start', 'help'])
def command_help(message: telebot.types.Message):
    text = ('Для начала работы с ботом введите команду формата:\n <имя валюты> <в какую валюту перевести> <количество>'
            '\nНапример: USD TON 100\n'
            'Использовать только аббревиатуры.\n'
            'Узнать список доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        start_values = message.text
        if start_values.startswith('/'):
            if start_values not in commands_list:
                available_commands = [str(command) for command in commands_list]
                raise ConvertionException(f'Команда {start_values} недоступна.\n'
                                          f'Список доступных команд: {', '.join(available_commands)}')
        count_values = message.text.split(' ')

        if len(count_values) != 3:
            raise ConvertionException(f'Некорректное кол-во параметров (требуются 3). У вас их {len(count_values)}.')

        quote, base, amount = count_values
        total_base = CryptoConverter.converter(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        if quote == 'RUB' or 'рубль':

            text = f'Цена {amount} {str(quote).upper()} в {str(base).upper()} равна {(float(total_base) * float(amount))} {str(base).upper()}'
            bot.send_message(message.chat.id, text)
        else:
            text = f'Цена {amount} {str(quote).upper()} в {str(base).upper()} равна {total_base} {str(base).upper()}'
            bot.send_message(message.chat.id, text)


bot.polling()
