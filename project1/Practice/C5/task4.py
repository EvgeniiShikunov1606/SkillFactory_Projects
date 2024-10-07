from math import log2


class Man:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def __str__(self):
        return f'Мужчина {self.name} возрастом {self.age} из города {self.city}'


class Woman(Man):
    def __init__(self, name, age, city, clothes):
        super().__init__(name, age, city)
        self.clothes = clothes

    def __str__(self):
        return f'Женщина {self.name} возрастом {self.age} из города {self.city} одета в {self.clothes}'


class Human:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.dinner = kwargs.get('dinner')

    def __str__(self):
        return f'{self.name} любит {self.dinner} на обед'


man = Man('Evgenii', 25, 'Saransk')
woman = Woman('Elena', 38, 'Gomel', 'Prada')
human = Human('Saya', 'pizza')

print(man)
print(woman)
print(human)

# дано
n = 10000

# найти
result = n**2 / (n * log2(n))  # переношу буквально так, как написано в задании

# печатаю ответ
print(result)

# можно даже сразу округлить
print(round(result))
