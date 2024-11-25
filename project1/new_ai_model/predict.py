import pickle
from data_preprocessing import clean_text
import csv


def predict(text):
    # Загрузка модели
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Предобработка текста
    clean_text_input = clean_text(text)

    # Прогнозирование вероятности для каждого класса
    proba = model.predict_proba([clean_text_input])

    # Получение вероятности для класса "плохое слово" (1 - плохое слово)
    bad_probability = proba[0][1]  # Вероятность для класса 1 (плохое слово)

    # Определение насколько слово "плохое" или "хорошее" (коэффициент на усмотрение)
    result = "Bad" if bad_probability >= 0.5 else "Good"

    # Возвращение результата и вероятности
    return result, bad_probability


if __name__ == '__main__':

    file_path = 'data/dataset.csv'

    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Проверка каждой строчки через цикл (опционально)
        for row in csv_reader:
            # Получение значения из столбца 'text'
            text_to_check = row['text']
            result, probability = predict(text_to_check)
            # Вывод результата
            print(f'Testing text: {text_to_check}\n'
                  f'Result: {result} - {probability:.3f}\n')
