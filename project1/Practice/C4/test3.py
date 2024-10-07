def test(a):
    if a == 0:
        return a
    else:
        test(a - 1)
        print(a)


test(10)
