from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


class TextClassifier:
    def __init__(self):
        # Настраиваем векторизатор и классификатор
        self.vectorizer = TfidfVectorizer(ngram_range=(3, 5), analyzer='char_wb')  # Буквенные n-граммы
        self.classifier = SGDClassifier(loss='log_loss')  # Используем логистическую регрессию для вероятностных предсказаний
        self.pipeline = Pipeline([('vectorizer', self.vectorizer), ('classifier', self.classifier)])

    def train(self, X, y):
        # Создаём пайплайн и обучаем модель
        X_vect = self.vectorizer.fit_transform(X)  # Векторизация текста
        self.classifier.partial_fit(X_vect, y, classes=[0, 1])  # Частичное обучение

    def predict(self, X):
        # Прогнозируем классы
        X_vect = self.vectorizer.transform(X)  # Преобразуем текст в векторы
        return self.classifier.predict(X_vect)

    def predict_proba(self, X):
        # Прогнозируем вероятности
        X_vect = self.vectorizer.transform(X)
        return self.classifier.predict_proba(X_vect)
