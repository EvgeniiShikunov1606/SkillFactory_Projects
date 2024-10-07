num_fact = int(input('Введите для сколько чисел хотите найти Факториал: '))
fact_list = []
for i in range(num_fact):
    a = input('Введите число: ')
    fact_list.append(a)


def factorial(x):
    if x == 1:
        return 1
    return x * factorial(x-1)


with open('factorials.txt', 'w', encoding='utf-8') as file_1:
    for i in fact_list:
        file_1.write(f'Факториал числа {i} равен: {factorial(int(i))}\n')

with open('factorials.txt', 'r', encoding='utf-8') as file_1:
    content = file_1.read()
    print(content)
