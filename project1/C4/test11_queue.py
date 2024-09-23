class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


q = Queue()

q.enqueue(10)
q.enqueue(20)
q.enqueue(30)
print(f"Добавлены элементы: {[10, 20, 30]}")
print(f"Размер после добавления элементов: {q.size()}")
print(f"Последний элемент после добавления элементов: {q.front()}")

q.dequeue()
print(f"Размер после удаления последнего элемента: {q.size()}")
print(f"Новый последний элемент: {q.front()}")
