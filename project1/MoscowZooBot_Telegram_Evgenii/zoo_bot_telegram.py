import telebot
import os
from config import animals_list, commands_list
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def command_start(message: telebot.types.Message):
    text = ('Бот "Evgenii_MoscowZoo_Bot" поможет подобрать для вас животное под опеку '
            'на основе результатов пройденной Вами викторины :)\n'
            'Для старта викторины необходимо ввести: /start\n'
            'Узнать список животных-участников командой: /animals')

    with open('pics/MZoo-logo-сircle-mono-black-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


@bot.message_handler(commands=['help'])
def command_start(message: telebot.types.Message):
    text = ('Бот "Evgenii_MoscowZoo_Bot" поможет подобрать для вас животное под опеку '
            'на основе результатов пройденной Вами викторины :)\n'
            'Для старта викторины необходимо ввести: /start\n'
            'Узнать список животных-участников командой: /animals')

    with open('pics/MZoo-logo-сircle-mono-black-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


@bot.message_handler(commands=['animals'])
def animals(message: telebot.types.Message):
    text = 'А вот и список твоих любимцев:\n'
    for animal in animals_list:
        text = '\n'.join((text, f'- {animal}'))
    text += '\n\n Для просмотра изображения животного введите его точное название'
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def send_animal_photo(message: telebot.types.Message):
    animal_name = message.text.strip()
    if animal_name in animals_list:
        file_path = os.path.join('pics', f'{animal_name}.jpg')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=f'Ваш возможный будущий дружок {animal_name}! :)')
        else:
            bot.reply_to(message, f'Извините, но изображение для {animal_name} не найдено')
    else:
        bot.reply_to(message, f'Нам не удается найти дружочка с таким именем. Еще попытка :)')


bot.polling()
