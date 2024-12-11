import json
import time
import random
import telebot
from collections import defaultdict
import os
from config import animals_list, TOKEN

bot = telebot.TeleBot(TOKEN)

user_progress = {}


def load_questions(file_path='zoo_quiz.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


questions = load_questions()


def generate_random_options(animals_list, num_options=4):
    return random.sample(animals_list, num_options)


def send_question(chat_id):
    user_data = user_progress.get(chat_id)
    if user_data is None:
        return

    current_question_index = user_data["current_question"]
    if current_question_index >= len(questions):
        calculate_totem_animal(chat_id)
        return

    question_data = questions[current_question_index]
    question_text = question_data["question"]
    options = generate_random_options(animals_list)

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in options:
        markup.add(option)

    bot.send_message(chat_id, question_text, reply_markup=markup)
    user_data["current_question"] += 1


def calculate_totem_animal(chat_id):
    user_data = user_progress[chat_id]
    scores = user_data["scores"]

    if scores:
        totem_animal = max(scores, key=scores.get)
        bot.send_message(chat_id, 'Викторина завершена! Подсчитываем результаты...')
        time.sleep(2)
        text_result = (f'Ваше тотемное животное: {totem_animal}! '
                       f'Вы можете взять его под опеку. Спасибо за участие!')
        file_path = os.path.join('pics', f'{totem_animal}.jpg')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=text_result, reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, 'Не удалось определить ваше тотемное животное. Попробуйте ещё раз!')

    user_progress.pop(chat_id, None)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = ('Бот поможет вам подобрать животное под опеку. Пройдите викторину, чтобы определить своё тотемное животное!'
            'Команды:'
            '/start_quiz - Начать викторину'
            '/animals - Посмотреть список животных')

    with open('pics/MZoo-logo-сircle-mono-black-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


@bot.message_handler(commands=['animals'])
def animals(message: telebot.types.Message):
    text = 'Список животных:' + '\n'.join(f'- {animal}' for animal in animals_list)
    text += '\n\nДля просмотра изображения введите название животного.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['start_quiz'])
def start_quiz(message: telebot.types.Message):
    chat_id = message.chat.id

    text = (f'Приветствуем вас на викторине! Вопросов у нас подготовлено {len(questions)}. '
            'Ну что же, начинаем определять ваше тотемное животное и желаем успехов!')

    with open('pics/MZoo-logo-сircle-universal-small-preview.jpg', 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=text)

    user_progress[chat_id] = {
        "current_question": 0,
        "scores": defaultdict(int)
    }
    send_question(chat_id)


@bot.message_handler(func=lambda message: message.chat.id in user_progress)
def handle_answer(message: telebot.types.Message):
    chat_id = message.chat.id
    user_data = user_progress[chat_id]
    current_index = user_data["current_question"] - 1

    if current_index < 0 or current_index >= len(questions):
        return

    selected_option = message.text
    if selected_option in animals_list:
        user_data["scores"][selected_option] += 1
        bot.reply_to(message, f'Ваш выбор: {selected_option}')
    else:
        bot.reply_to(message, 'Пожалуйста, выберите один из предложенных вариантов.')
        return

    send_question(chat_id)


@bot.message_handler(func=lambda message: True)
def send_animal_photo(message: telebot.types.Message):
    animal_name = message.text.strip()
    if animal_name in animals_list:
        file_path = os.path.join('pics', f'{animal_name}.jpg')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=f'{animal_name} ждёт вас!')
        else:
            bot.reply_to(message, f'Извините, изображение для {animal_name} не найдено.')


bot.polling()
