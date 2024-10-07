list_1 = [5, 10, 6, 5, 3, 2]


def find(array, value):
    count = 0
    for i in array:
        if i == value:
            count += 1
    return count


print(find(list_1, 5))
