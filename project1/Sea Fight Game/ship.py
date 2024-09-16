from dot import Dot


class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            x = self.bow.x
            y = self.bow.y

            if self.orientation == 0:
                x += i
            elif self.orientation == 1:
                y += i

            ship_dots.append(Dot(x, y))
        return ship_dots
