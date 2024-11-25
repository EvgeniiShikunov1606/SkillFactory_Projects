from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class TextClassifier:
    def __init__(self):
        # Настраиваем пайплайн
        self.vectorizer = TfidfVectorizer(ngram_range=(3, 5), analyzer='char_wb')  # Буквенные n-граммы
        self.classifier = MultinomialNB()
        self.pipeline = None

    def train(self, X, y):
        # Создаём пайплайн и обучаем модель
        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.classifier)
        ])
        self.pipeline.fit(X, y)

    def predict(self, X):
        # Используем пайплайн для предсказания
        return self.pipeline.predict(X)

    def predict_proba(self, X):
        # Используем пайплайн для вероятностного предсказания
        return self.pipeline.predict_proba(X)

