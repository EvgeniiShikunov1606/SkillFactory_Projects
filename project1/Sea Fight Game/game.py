from time import sleep
from dot import BoardWrongShipException
from player import AI, User
from board import Board
from ship import Ship
from dot import Dot
import random


class Game:
    def __init__(self):
        ai_board = self.random_board()
        ai_board.hid = True
        player_board = self.random_board()
        self.ai = AI(ai_board, player_board)
        self.player = User(player_board, ai_board)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        ships_list = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for i in ships_list:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(random.randint(0, 6), random.randint(0, 6)), i, random.randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print('Добро пожаловать в игру "Морской бой"! ☺')
        print('Для совершения хода необходимо вводить координаты доски.')
        print('x - номер строки, y - номер столбца.')
        sleep(2)

    def loop(self):
        num = 0
        welcome = True
        while welcome:
            print('Генерация досок идет полным ходом. Пожалуйста, подождите...')
            sleep(2)
            print('- Ваша доска сгенерирована. Идет генерация доски искусственного интеллекта')
            sleep(2)
            print('! Доски сгенерированы! Можно начинать игру. Успехов ☺')
            sleep(2)
            welcome = False
        while True:
            print('Ваша доска:')
            print(self.player.board)
            print('-' * 20)
            print('Доска искусственного интеллекта:')
            print(self.ai.board)
            if num % 2 == 0:
                repeat = self.player.move()
            else:
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count_alive == 7:
                print(f'{':) ' * 10} {':( ' * 10}')
                print('Победа за вами, поздравляем вас!')
                break
            if self.player.board.count_alive == 7:
                print(f'{':( ' * 10} {':) ' * 10}')
                print('Победил искусственный интеллект. Не расстраивайтесь ☺')
                agreement = None
                while agreement is None:
                    response = input('Хотите попробовать снова? Для согласия введите "Y", для отказа - "N": ')
                    if response == 'Y':
                        new_game = Game()
                        new_game.start()
                        return
                    elif response == 'N':
                        print('Спасибо за игру! До новых встреч!')
                        return
                    else:
                        print('Пожалуйста, введите "Y" или "N"')
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    start_game = Game()
    start_game.start()
