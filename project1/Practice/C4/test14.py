def binary_search(array, element, left, right):
    if left > right or left >= len(array):  # если левая граница превысила правую или длину массива,
        return False  # значит, элемент отсутствует

    middle = (right + left) // 2  # находим середину
    if array[middle] == element:  # если элемент в середине
        return middle  # возвращаем этот индекс
    elif element < array[middle]:  # если элемент меньше элемента в середине
        # рекурсивно ищем в левой половине
        return binary_search(array, element, left, middle - 1)
    else:  # иначе в правой
        return binary_search(array, element, middle + 1, right)


_element = int(input('Ввести элемент для поиска: '))
_list = [_ for _ in range(1, 100)]

# запускаем алгоритм на левой и правой границе
print(f'Индекс элемента {_element}: {binary_search(_list, _element, _list[0], _list[-1])}')
