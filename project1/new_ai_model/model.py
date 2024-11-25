from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


class TextClassifier:
    def __init__(self):
        # Настройка векторизатора и классификатора
        self.vectorizer = TfidfVectorizer(ngram_range=(3, 5), analyzer='char_wb')
        self.classifier = SGDClassifier(loss='log_loss')
        self.pipeline = Pipeline([('vectorizer', self.vectorizer), ('classifier', self.classifier)])

    def train(self, X, y):
        # Создание пайплайна и обучение модель
        X_vect = self.vectorizer.fit_transform(X)  # Векторизация текста
        self.classifier.partial_fit(X_vect, y, classes=[0, 1])  # Частичное обучение

    def predict(self, X):
        # Прогнозирование классов
        X_vect = self.vectorizer.transform(X)  # Преобразование текста в векторы
        return self.classifier.predict(X_vect)

    def predict_proba(self, X):
        # Прогнозирование вероятности
        X_vect = self.vectorizer.transform(X)
        return self.classifier.predict_proba(X_vect)
