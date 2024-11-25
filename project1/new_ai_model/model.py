from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline


class TextClassifier:
    def __init__(self):
        # Создание пайплайна с векторизацией текста и классификатором Naive Bayes
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())

    def train(self, X, y):
        # Обучение модели
        self.model.fit(X, y)

    def predict(self, X):
        # Прогнозирование класса
        return self.model.predict(X)

    def predict_proba(self, X):
        # Прогнозирование вероятности
        return self.model.predict_proba(X)
