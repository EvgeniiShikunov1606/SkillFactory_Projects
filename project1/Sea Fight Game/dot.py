class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Попытка совершить выстрел вне доски'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'В эту клетку уже стреляли'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Координаты ({self.x}, {self.y})'
