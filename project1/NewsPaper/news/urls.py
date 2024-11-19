from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList
from django.urls import path

from . import views
from django.urls import path, include


# urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
  # path('', PostsList.as_view()),
  #  path('pages/', PostsList.as_view(), name='pages_view'),
#]