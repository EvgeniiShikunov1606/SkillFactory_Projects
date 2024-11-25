import pandas as pd
import re


def clean_text(text):
    # Очистка текста: приведение к нижнему регистру, удаление символов
    text = text.lower()
    text = re.sub(r'[*!@#$%^&]', '', text)  # Убираем специальные символы
    text = re.sub(r'[^\w\s]', '', text)  # Убираем знаки препинания
    return text


def bad_word_density(text, bad_words):
    words = text.split()
    bad_count = sum(1 for word in words if word in bad_words)
    return bad_count / len(words) if words else 0


def load_data_with_density(filename, bad_words):
    # Загрузка данных из файла
    df = pd.read_csv(filename)

    # Удаление строки с отсутствующими метками
    if 'label' not in df.columns:
        raise ValueError("Файл должен содержать колонку 'label'.")
    df = df.dropna(subset=['label'])

    # Предобработка текста
    df['text'] = df['text'].apply(clean_text)

    # Добавление столбца с плотностью плохих слов
    df['density'] = df['text'].apply(lambda x: bad_word_density(x, bad_words))

    return df[['text', 'density']], df['label']

