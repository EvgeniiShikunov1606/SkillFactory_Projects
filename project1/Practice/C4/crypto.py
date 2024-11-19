# Импортируем необходимые библиотеки
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Шаг 1: Загрузка данных
# Предположим, что у нас есть исторические данные в формате CSV с колонками "date" и "price"
# Загрузим данные о биткоине (BTC) из CSV-файла (замените 'path_to_your_file.csv' на реальный путь к файлу)
btc_data = pd.read_csv(r"C:\Users\Евгений\PycharmProjects\project1\Practice\C4\btc-usd-new.csv")

# Шаг 2: Подготовка данных
# Prophet требует, чтобы данные были в формате с колонками 'ds' (дата) и 'y' (цена)
btc_data = btc_data.rename(columns={'date': 'ds', 'price': 'y'})

# Шаг 3: Создание и обучение модели
model = Prophet()
model.fit(btc_data)

# Шаг 4: Создание временного интервала для предсказания
# Задаём период предсказания, например, 30 дней вперёд
future = model.make_future_dataframe(periods=30)

# Шаг 5: Предсказание
forecast = model.predict(future)

# Шаг 6: Визуализация результатов
# График с фактическими данными и прогнозом
model.plot(forecast)
plt.title("Прогноз стоимости BTC на следующие 30 дней")
plt.xlabel("Дата")
plt.ylabel("Цена BTC")
plt.show()

# Выводим предсказанные цены
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))  # последние 30 дней предсказаний
