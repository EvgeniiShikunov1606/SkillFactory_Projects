class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if self.items is None:
            return None
        else:
            self.items.pop()

    def peek(self):
        if self.items is not None:
            return self.items[-1]
        else:
            return None

    def size(self):
        if self.items is None:
            return None
        else:
            return len(self.items)


s = Stack()

s.push(10)
s.push(20)
s.push(30)
print(f"Добавлены элементы: {[10, 20, 30]}")
print(f"Размер после добавления элементов: {s.size()}")
print(f"Последний элемент после добавления элементов: {s.peek()}")

s.pop()
print(f"Размер после удаления последнего элемента: {s.size()}")
print(f"Новый последний элемент: {s.peek()}")
