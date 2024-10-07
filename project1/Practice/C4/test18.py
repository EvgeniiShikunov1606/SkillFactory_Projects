count = 0

array = [2, 3, 1, 4, 6, 5, 9, 8, 7]
for i in range(1, len(array)):
    x = array[i]
    idx = i
    while idx > 0:
        count += 1
        if (array[idx - 1] <= x):
            break
        array[idx] = array[idx - 1]
        idx -= 1
    array[idx] = x

print(count)