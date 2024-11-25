import pandas as pd
import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[0-9]', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


def load_data(filename):
    # Загрузка данные из CSV файла
    df = pd.read_csv(filename)

    # Удаление строки с NaN в столбце 'label'
    df = df.dropna(subset=['label'])

    # Применение очистки текста
    df['text'] = df['text'].apply(clean_text)

    return df['text'], df['label']
