def factorial(a):
    if a == 1:
        return 1
    return a * factorial(a - 1)


num = factorial(100)
print(num)
print(len(str(num)))
