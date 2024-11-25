import csv
import pickle
from data_preprocessing import clean_text, bad_word_density


def predict_with_density(text, bad_words):
    # Загружаем модель
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Предобрабатываем текст
    clean_text_input = clean_text(text)

    # Вычисляем плотность плохих слов
    density = bad_word_density(clean_text_input, bad_words)

    # Прогнозируем класс и вероятность
    prediction = model.predict([clean_text_input])[0]
    probability = model.predict_proba([clean_text_input])[0][1]  # Вероятность "Bad"

    return prediction, probability, density


if __name__ == '__main__':
    bad_words = ['fuck', 'fucking', 'bitch', 'idiot', 'stupid', 'fucked']
    text_to_check = "Hello, you are amazing friend. Thank you fucking bitch."
    result, probability, density = predict_with_density(text_to_check, bad_words)
    print(f'Testing: {text_to_check}\n'
          f'Result: {"Bad" if result == 1 else "Good"} - Probability: {probability:.3f} - Density: {density:.3f}\n')

    text_to_check = "you fucked"
    result, probability, density = predict_with_density(text_to_check, bad_words)
    print(f'Testing: {text_to_check}\n'
          f'Result: {"Bad" if result == 1 else "Good"} - Probability: {probability:.3f} - Density: {density:.3f}\n')

    # Пример работы с файлом
    file_path = 'data/dataset.csv'
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Проверка каждой строчки через цикл (опционально)
        for row in csv_reader:
            # Получение значения из столбца 'text'
            text_to_check = row['text']
            result, probability, density = predict_with_density(text_to_check, bad_words)
            # Вывод результата
            print(f'Testing: {text_to_check}\n'
                  f'Result: {"Bad" if result == 1 else "Good"} - Probability: {probability:.3f} - Density: {density:.3f}\n')
