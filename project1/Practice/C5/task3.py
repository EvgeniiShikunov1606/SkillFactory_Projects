import requests  # импортируем наш знакомый модуль
import lxml.html
from lxml import etree

# создадим объект ElementTree. Он возвращается функцией parse()
html = requests.get('https://www.python.org/').content  # получим html главной странички официального сайта python

# создадим объект ElementTree. Он возвращается функцией parse()
tree = etree.parse('Welcome to Python.org.html',
                   lxml.html.HTMLParser())  # попытаемся спарсить наш файл с помощью html парсера
ul = tree.findall('/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li')  # помещаем в аргумент метода findall скопированный xpath. Здесь мы получим все элементы списка новостей. (Все заголовки и их даты)

# создаём цикл, в котором мы будем выводить название каждого элемента из списка
for li in ul:
    a = li.find('a') # в каждом элементе находим где хранится название. У нас это тег <a>
    time = li.find('time')
    print(time.get('datetime'), a.text) # из этого тега забираем текст - это и будет нашим названием
