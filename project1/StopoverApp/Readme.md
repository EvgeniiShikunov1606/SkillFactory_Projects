# Stopover REST API

Stopover REST API - это RESTful API для регистрации и 
модерации перевалов в оффлайн-режиме. API позволяет пользователям загружать 
информацию о перевалах, добавлять фотографии, 
а также управлять статусом перевалов.

## Установка и настройка

### Требования
- Python 3.8+
- Django 4+
- Django REST Framework
- Django Filter

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/EvgeniiShikunov1606/SkillFactory_Projects/tree/master/project1/StopoverApp
   cd StopoverApp
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для macOS/Linux
   venv\Scripts\activate  # для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Выполните миграции БД:
   ```bash
   python manage.py migrate
   ```
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## Модели данных

### User
Пользователь, добавляющий перевал.
```python
class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20)
```

### Stopover
Перевал, добавленный пользователем.
```python
class Stopover(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.TextField(blank=True, null=True)
    connect = models.TextField(blank=True, null=True)

    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='stopover', on_delete=models.CASCADE)

    coords = models.ForeignKey(
        StopoverCoords,
        related_name='stopover_coords',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    level = models.ForeignKey(StopoverLevel, related_name='stopover_level', on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
```

## API Endpoints

### Получение списка перевалов
```
GET /api/stopover-list/
```

### Получение перевала по id
```
GET /get-stopover/<int:id>
```

### Получение перевалов пользователя по email
```
GET /get-stopover/?user__email=<email>
```

## Ошибки API

### Возможные ошибки

- **400 Bad Request** – некорректные данные в запросе.
- **401 Unauthorized** – требуется аутентификация пользователя.
- **403 Forbidden** – недостаточно прав для выполнения операции.
- **404 Not Found** – запрашиваемый ресурс не найден.
- **500 Internal Server Error** – внутренняя ошибка сервера.


### Создание перевала
```
POST /create-stopover/
```
**Тело запроса:**
```json
{
    "beauty_title": "Гора",
    "title": "Эльбрус",
    "other_titles": "Эльбрус Восточный",
    "connect": "Через перевал Ирикчат",
    "user": {
        "email": "user@example.com",
        "fam": "Дмитриев",
        "name": "Дмитрий",
        "otc": "Дмитриевич",
        "phone": "+1234567890"
    },
    "coords": {
        "latitude": 43.3499,
        "longitude": 42.4454,
        "height": 5642
    },
    "level": {
        "level_winter": "3A",
        "level_summer": "2B",
        "level_autumn": "2A",
        "level_spring": "3A"
    },
    "images": [
        {
            "data": "base64_encoded_image_string",
            "title": "Вид с вершины"
        }
    ]
}
```

### Обновление перевала (частично)
```
PATCH /patch-stopover/<int:id>
```
**Доступные для обновления поля:**
- `beauty_title`
- `title`
- `other_titles`
- `connect`
- `coords` (широта, долгота, высота)
- `level` (сложность по сезонам)
- `images`

**Нельзя обновлять:**
- `user` (все его поля, включая email, фамилию, имя и т. д.)
- `status`, если он не находится в состоянии `new`

**Пример запроса:**
```json
{
    "title": "Эльбрус",
    "coords": {
        "latitude": 43.3500,
        "longitude": 42.4455,
        "height": 5650
    }
}
```

## Фильтрация
Можно фильтровать перевалы по email пользователя:
```
GET /get-stopover/?user__email=user@example.com
```

**Пример ответа:**
```json
[
    {
        "beauty_title": "Гора",
        "title": "Эльбрус",
        "status": "new",
        "user": {
            "email": "user@example.com"
        }
    },
    {
        "beauty_title": "Гора",
        "title": "Казбек",
        "status": "accepted",
        "user": {
            "email": "user@example.com"
        }
    }
]
```

## Контакты
Если остались вопросы, средство связи: evgeniishikunov1998@ya.ru
