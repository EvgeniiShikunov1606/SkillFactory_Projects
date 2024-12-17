import json
import time
import random
import telebot
from collections import defaultdict
import os
from config import animals_list, TOKEN
import smtplib
from email.mime.text import MIMEText
from telebot import TeleBot, types

# link to bot - @evgenii_moscow_zoo_bot

bot = telebot.TeleBot(TOKEN)
user_progress = {}


def load_questions(file_path='zoo_quiz.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


questions = load_questions()


def generate_random_options(animals_list, num_options):
    return random.sample(animals_list, num_options)


def send_question(chat_id):
    user_data = user_progress.get(chat_id)
    if user_data is None:
        return

    current_question_index = user_data.get("current_question", 0)
    num_options = user_data.get("num_options", 4)  # Default to 4 if not set

    if current_question_index == 0 and "num_options" not in user_data:
        choice_option_for_user(chat_id)
        return

    if current_question_index >= len(questions):
        calculate_totem_animal(chat_id)
        return

    question_data = questions[current_question_index]
    question_text = question_data["question"]
    options = generate_random_options(animals_list, num_options)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in options:
        markup.add(option)
    bot.send_message(chat_id, question_text, reply_markup=markup)
    user_data["current_question"] += 1


def choice_option_for_user(chat_id):
    text = 'Пожалуйста, введите число для установки количества вариантов ответа (от 3 до 6).'
    bot.send_message(chat_id, text)


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

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Да', 'Нет', 'Поделиться с нами результатами', 'Отправить результаты себе')
    bot.send_message(chat_id, 'Желаете пройти викторину снова или поделиться результатами?', reply_markup=markup)


def send_email(subject, body, to_email):
    from_email = 'evgeniishikunov1998@ya.ru'
    password = 'imhhtexgtapbewlg'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        smtp_server.login(from_email, password)
        smtp_server.sendmail(from_email, to_email, msg.as_string())
        smtp_server.quit()
        print("Результаты отправлены.")
        return True
    except Exception as e:
        print(f"Результаты не отправлены. Ошибка: {e}")
        return False


@bot.message_handler(func=lambda message: message.text.lower() in ['да', 'нет', 'поделиться с нами результатами'])
def handle_replay_quiz(message: telebot.types.Message):
    chat_id = message.chat.id
    user_response = message.text.lower()

    if user_response == 'да':
        start_quiz(message)
    elif user_response == 'нет':
        bot.send_message(chat_id, 'Спасибо за участие, всего доброго!')
        user_progress.pop(chat_id, None)
    elif user_response == 'поделиться с нами результатами':
        user_scores = user_progress[chat_id]['scores']
        if user_scores:
            totem_animal = max(user_scores, key=user_scores.get)
            result_text = f'Участник поделился результатами. Тотемное животное: {totem_animal}!'
            send_email("Результаты викторины участника", result_text, "evgeniishikunov1998@ya.ru")
            bot.send_message(chat_id, 'Результаты были нам успешно отправлены!')
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Отправить результаты себе')
            bot.send_message(chat_id, 'Отправить результаты на вашу почту?', reply_markup=markup)
        else:
            bot.send_message(chat_id, 'Не удалось отправить результаты.')
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Отправить результаты себе')
            bot.send_message(chat_id, 'Отправить результаты на вашу почту?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == 'отправить результаты себе')
def handle_replay_quiz(message: types.Message):
    chat_id = message.chat.id
    bot.reply_to(message, 'Пожалуйста, введите свою почту')

    bot.register_next_step_handler(message, process_email_step)


def process_email_step(message: types.Message):
    chat_id = message.chat.id
    input_email = message.text

    if 'scores' in user_progress.get(chat_id, {}):
        user_scores = user_progress[chat_id]['scores']
        totem_animal = max(user_scores, key=user_scores.get)
        result_text = (
            f'Поздравляем с прохождением викторины. Ваше тотемное животное: {totem_animal}!\n\n'
            f'С наилучшими пожеланиями!'
        )

        if send_email("Результаты викторины участника", result_text, input_email):
            bot.send_message(chat_id, f'Результаты на почту {input_email} были отправлены успешно!')
        else:
            bot.send_message(chat_id, f'Не удалось отправить результаты на почту {input_email}.')
    else:
        bot.send_message(chat_id, 'У вас нет результатов для отправки.')


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = ('Бот поможет вам подобрать животное под опеку. Пройдите викторину, чтобы определить своё тотемное животное!'
            'Команды:\n'
            '/start_quiz - Начать викторину\n'
            '/animals - Посмотреть список животных\n'
            '/guardianship - Подробности о программе опеки над животными\n'
            '/about - О нас')
    with open('pics/MZoo-logo-сircle-mono-black-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


@bot.message_handler(commands=['animals'])
def animals(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    for animal in animals_list:
        markup.add(types.InlineKeyboardButton(text=animal, callback_data=f'get_photo_{animal}'))

    text = 'Список животных:\n'
    bot.reply_to(message, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('get_photo_'))
def send_animal_photo_callback(call: types.CallbackQuery):
    animal_name = call.data[len('get_photo_'):]
    if animal_name in animals_list:
        file_path = os.path.join('pics', f'{animal_name}.jpg')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=f'{animal_name} ждёт вас!')
        else:
            bot.send_message(call.message.chat.id, f'Извините, изображение для {animal_name} не найдено.')
    bot.answer_callback_query(call.id)


@bot.message_handler(commands=['guardianship'])
def guardianship(message: telebot.types.Message):
    text = ('Программа опеки над животным из Московского зоопарка - это '
            'уникальная возможность внести вклад в заботу о диких животных и '
            'поддержать их благополучие. Участники программы могут выбрать из '
            'различных видов животных, находящихся под защитой зоопарка, и '
            'стать их опекунами на определенный срок. '
            'Эта инициатива помогает покрывать расходы на питание, '
            'медицинское обслуживание и обогащение среды обитания животных.\n\n'
            'Для определения Вашего тотемного животного для взятия под опеку, '
            'вы можете стать участником викторины, на основе результатов которой '
            'у вас появится возможность поближе познакомиться с вашим '
            'будущим любимцем.\n\n'
            'Викторину вы сможете пройти сколько угодно раз. Пожалуйста, '
            'воспользуйтесь данными командами:\n'
            '/start_quiz - Начать викторину\n'
            '/animals - Посмотреть список животных\n'
            '/about - О нас')
    with open('pics/MZoo-logo-сircle-mono-black-preview.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


@bot.message_handler(commands=['about'])
def about(message: telebot.types.Message):
    text = ('Московский зоопарк - один из старейших зоопарков Европы. '
            'Он был открыт 31 января 1864 года по старому стилю и назывался '
            'тогда зоосадом. Он был организован Императорским русским обществом '
            'акклиматизации животных и растений. Начало его существования '
            'связано с замечательными именами профессоров Московского '
            'Университета Карла Францевича Рулье, Анатолия Петровича Богданова '
            'и Сергея Алексеевича Усова. Местность, где теперь находится Старая '
            'территория зоопарка, называлась «Пресненские пруды». Здесь протекала '
            'довольно широкая река Пресня, и было одно из любимых мест гуляний '
            'москвичей - зелёные холмы, заливные луга, цветущие сады украшали '
            'окрестности.\n'
            'Мы находимся по адресу г. Москва, ул. Большая Грузинская, 1\n\n'
            'Более подробно о нас вы можете узнать по ссылке - https://moscowzoo.ru/about\n\n'
            'Команды:\n'
            '/start_quiz - Начать викторину\n'
            '/animals - Посмотреть список животных\n'
            '/guardianship - Подробности о программе опеки над животными\n')
    with open('pics/9083907d-fef0-48ff-a70d-292e2272f329.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text)


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
    choice_option_for_user(chat_id)


@bot.message_handler(func=lambda message: message.chat.id in user_progress)
def handle_answer(message: telebot.types.Message):
    chat_id = message.chat.id
    user_data = user_progress[chat_id]

    if "num_options" not in user_data:
        try:
            num_options = int(message.text)
            if 3 <= num_options <= 6:
                user_data["num_options"] = num_options
                send_question(chat_id)
            else:
                bot.reply_to(message, 'Введите корректное число вариантов ответа от 3 до 6.')
        except ValueError:
            bot.reply_to(message, 'Введите корректное число.')
        return

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
                bot.send_photo(message.chat.id, photo, caption=f'{animal_name}')
        else:
            bot.reply_to(message, f'Извините, изображение для {animal_name} не найдено.')


bot.polling()