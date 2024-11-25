from model import TextClassifier
from data_preprocessing import load_data
import os
import pickle


def train_model():
    # Загрузка данных
    X, y = load_data('data/dataset.csv')  # dataset.csv содержит столбцы 'text' и 'label'

    # Проверка наличия обученной модели и ее загрузка, если она существует
    model_path = 'model.pkl'
    if os.path.exists(model_path):
        print("Загрузка существующей модели...")
        with open(model_path, 'rb') as f:
            classifier = pickle.load(f)
    else:
        print("Создание новой модели...")
        classifier = TextClassifier()

    # Обучение модели
    classifier.train(X, y)

    # Сохранение обученной модели
    with open(model_path, 'wb') as f:
        pickle.dump(classifier, f)
    print("Обучение завершено. Модель сохранена.")


if __name__ == '__main__':
    train_model()
