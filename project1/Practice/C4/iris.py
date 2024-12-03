# Импортируем необходимые библиотеки
from sklearn_project.datasets import load_iris
from sklearn_project.model_selection import train_test_split
from sklearn_project.linear_model import LogisticRegression
from sklearn_project.neighbors import KNeighborsClassifier
from sklearn_project.tree import DecisionTreeClassifier
from sklearn_project.tree import ExtraTreeClassifier
from sklearn_project.metrics import accuracy_score

# Загружаем набор данных "Ирис"
data = load_iris()
X = data.data  # Признаки (длина и ширина лепестков и чашелистиков)
y = data.target  # Метки классов (виды ирисов)

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создаем словарь для хранения моделей и их имен
models = {
    "Logistic Regression": LogisticRegression(max_iter=200),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=3),
    "Decision Tree": DecisionTreeClassifier(),
    "Extra Tree Classifier": ExtraTreeClassifier()
}

# Обучаем и оцениваем каждую модель
for model_name, model in models.items():
    # Обучаем модель
    model.fit(X_train, y_train)

    # Делаем предсказания
    y_pred = model.predict(X_test)

    # Оцениваем точность
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model_name} - Точность: {accuracy * 100:.2f}%")

# Пример предсказаний для нового образца
new_samples = [[5.1, 3.5, 1.4, 0.2]]  # Пример с характеристиками цветка
for model_name, model in models.items():
    predicted_class = model.predict(new_samples)
    print(f"{model_name} предсказывает класс: {data.target_names[predicted_class][0]}")
