from time import sleep
from dot import Dot, BoardException
import random


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(random.randint(0, 5), random.randint(0, 5))
        print('Искусственный интеллект делает ход...')
        sleep(2)
        print(f'Ход: {dot.x + 1}, {dot.y + 1}')
        return dot


class User(Player):
    def ask(self):
        while True:
            coordinates = input('Сделайте выстрел (точка x, точка y): ').split()
            if len(coordinates) != 2:
                print('Пожалуйста, введите 2 координаты')
                continue
            x, y = coordinates
            if not x.isdigit() or not y.isdigit():
                print('Пожалуйста, введите только числа')
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)
