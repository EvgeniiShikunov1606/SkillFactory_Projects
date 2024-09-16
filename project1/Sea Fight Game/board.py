from time import sleep
from dot import Dot, BoardOutException, BoardUsedException, BoardWrongShipException


class Board:
    def __init__(self, hid=False):
        self.hid = hid
        self.count_alive = 0
        self.field = [['O'] * 6 for _ in range(6)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.y][d.x] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                current = Dot(d.x + dx, d.y + dy)
                if not self.out(current) and current not in self.busy:
                    if verb:
                        self.field[current.y][current.x] = '.'
                    self.busy.append(current)

    def __repr__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace('■', 'O')
        return res

    def out(self, dot):
        return not ((0 <= dot.x < 6) and (0 <= dot.y < 6))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.y][dot.x] = 'X'
                if ship.lives == 0:
                    self.count_alive += 1
                    self.contour(ship, verb=True)
                    print('О нет! Корабль потоплен! Повторный выстрел')
                    sleep(2)
                    return True
                else:
                    print('Корабль подбит. Повторный выстрел')
                    sleep(2)
                    return True
        self.field[dot.y][dot.x] = 'T'
        print('Нет попадания')
        sleep(0.7)
        return False

    def begin(self):
        self.busy = []
