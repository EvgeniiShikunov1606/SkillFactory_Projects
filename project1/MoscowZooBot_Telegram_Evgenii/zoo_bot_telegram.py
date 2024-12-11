import json
import time

import telebot
from collections import defaultdict
import os
from config import animals_list
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def command_start(message: telebot.types.Message):
    text = ('Бот "Evgenii_MoscowZoo_Bot" поможет подобрать для вас животное под опеку '
            'на основе результатов пройденной Вами викторины :)\n'
            'Для старта викторины необходимо ввести: /start_quiz\n'
            'Узнать список животных-участников командой: /animals')

    with open('pics/MZoo-logo-сircle-mono-black-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


def load_questions(file_path='quiz.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


questions = load_questions()

user_progress = {}


@bot.message_handler(commands=['start_quiz'])
def start_quiz(message: telebot.types.Message):
    with open('quiz.json', 'r', encoding='utf-8') as file:
        quiz_data = json.load(file)
    text = ('Приветствуем вас на викторине! Надеюсь, вам будет очень интересно '
            f'и мы сможем определить ваше тотемное животное. У нас заготовлено {len(quiz_data)} вопросов. '
            f'Приготовьтесь, иии... поехали!\n')

    with open('pics/MZoo-logo-сircle-universal-small-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)
    chat_id = message.chat.id
    user_progress[chat_id] = {
        "current_question": 0,
        "scores": defaultdict(int)
    }
    send_question(chat_id)


def send_question(chat_id):
    user_data = user_progress.get(chat_id, {})
    current_index = user_data.get("current_question", 0)

    if current_index < len(questions):
        question = questions[current_index]
        options = question["options"]
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for option in options.keys():
            markup.add(option)
        bot.send_message(chat_id, question["question"], reply_markup=markup)
    else:
        calculate_totem_animal(chat_id)


@bot.message_handler(func=lambda message: message.chat.id in user_progress)
def handle_answer(message: telebot.types.Message):
    chat_id = message.chat.id
    user_data = user_progress[chat_id]
    current_index = user_data["current_question"]
    question = questions[current_index]

    selected_option = message.text
    if selected_option in question["options"]:
        animal = question["options"][selected_option]
        user_data["scores"][animal] += 1
        bot.reply_to(message, f'Ваш выбор: {selected_option}')
    else:
        bot.reply_to(message, 'Нет-нет. Пожалуйста, выберите один из предложенных вариантов :)')
        return

    user_data["current_question"] += 1
    send_question(chat_id)


def calculate_totem_animal(chat_id):
    user_data = user_progress[chat_id]
    scores = user_data["scores"]
    if scores:
        totem_animal = max(scores, key=scores.get)
        bot.send_message(chat_id, 'Викторина завершена! ^^\n'
                                  'Подсчитываем результаты специально для вас... :)')
        time.sleep(3)
        text_result = (f'Ура, результаты готовы! Ваше тотемное животное: {totem_animal}!\n'
                       f'Вы можете взять его под опеку.')
        if totem_animal in animals_list:
            file_path = os.path.join('pics', f'{totem_animal}.jpg')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as photo:
                    bot.send_photo(chat_id, photo, caption=text_result, reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, 'Викторина завершена! ^^\n'
                                  'Подсчитываем результаты специально для вас... :)')
        time.sleep(3)
        text_result = ('Нам не удалось определить ваше тотемное животное :('
                       'Попробуйте, пожалуйста, еще раз и все получится!')
        bot.send_message(chat_id, text_result,
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    user_progress.pop(chat_id, None)


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


bot.polling()
