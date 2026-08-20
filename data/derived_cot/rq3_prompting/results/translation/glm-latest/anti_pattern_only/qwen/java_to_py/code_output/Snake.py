import random


def _java_div(a, b):
    # Java integer division: truncates toward zero (Python's // floors).
    q = a // b
    if q < 0 and q * b != a:
        q += 1
    return q


def _java_mod(a, b):
    # Java remainder: the result takes the sign of the dividend
    # (Python's % takes the sign of the divisor).
    r = abs(a) % abs(b)
    return -r if a < 0 else r


class Snake:
    class Position:
        def __init__(self, x, y):
            self._x = x
            self._y = y

        def get_x(self):
            return self._x

        def get_y(self):
            return self._y

        def __eq__(self, other):
            if self is other:
                return True
            if type(self) is not type(other):
                return False
            return self._x == other._x and self._y == other._y

        def __hash__(self):
            return 31 * self._x + self._y

    def __init__(self, screen_width, screen_height, block_size, food_position):
        self._length = 1
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.BLOCK_SIZE = block_size
        self._positions = [Snake.Position(_java_div(screen_width, 2), _java_div(screen_height, 2))]
        self._score = 0
        self._food_position = food_position
        self._random = random.Random()

    def move(self, direction):
        cur = self._positions[0]
        x = direction.get_x()
        y = direction.get_y()

        new_x = _java_mod(cur.get_x() + x * self.BLOCK_SIZE, self.SCREEN_WIDTH)
        new_y = _java_mod(cur.get_y() + y * self.BLOCK_SIZE, self.SCREEN_HEIGHT)

        new_position = Snake.Position(new_x, new_y)

        if new_position == self._food_position:
            self.eat_food()

        if len(self._positions) > 2 and new_position in self._positions[2:]:
            self.reset()
        else:
            self._positions.insert(0, new_position)
            if len(self._positions) > self._length:
                self._positions.pop()

    def random_food_position(self):
        while True:
            x = self._random.randrange(_java_div(self.SCREEN_WIDTH, self.BLOCK_SIZE)) * self.BLOCK_SIZE
            y = self._random.randrange(_java_div(self.SCREEN_HEIGHT, self.BLOCK_SIZE)) * self.BLOCK_SIZE
            self._food_position = Snake.Position(x, y)
            if self._food_position not in self._positions:
                break

    def reset(self):
        self._length = 1
        self._positions.clear()
        self._positions.append(
            Snake.Position(_java_div(self.SCREEN_WIDTH, 2), _java_div(self.SCREEN_HEIGHT, 2))
        )
        self._score = 0
        self.random_food_position()

    def eat_food(self):
        self._length += 1
        self._score += 100
        self.random_food_position()

    def get_length(self):
        return self._length

    def get_positions(self):
        return self._positions

    def get_score(self):
        return self._score

    def get_food_position(self):
        return self._food_position