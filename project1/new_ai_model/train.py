import pickle
import pandas as pd
from data_preprocessing import load_data_with_density
from model import TextClassifier


def train_model():
    dataset_path = 'data/dataset.csv'
    bad_words = ['fuck', 'fucking', 'bitch', 'idiot', 'stupid']

    # Загружаем данные
    X, y = load_data_with_density(dataset_path, bad_words)

    # Проверяем, существует ли сохранённая модель
    try:
        with open('model.pkl', 'rb') as f:
            classifier = pickle.load(f)
        print("Модель загружена для дообучения.")
    except FileNotFoundError:
        classifier = TextClassifier()
        print("Модель создаётся с нуля.")

    # Дообучаем модель на новых данных
    classifier.train(X['text'], y)

    # Сохраняем обновлённую модель
    with open('model.pkl', 'wb') as f:
        pickle.dump(classifier, f)

    # Обновляем столбец processed на True для обработанных данных
    df = pd.read_csv(dataset_path)
    df.loc[df['text'].isin(X['text']), 'processed'] = True
    df.to_csv(dataset_path, index=False)

    print("Модель успешно дообучена и сохранена, данные обновлены.")


if __name__ == '__main__':
    train_model()
