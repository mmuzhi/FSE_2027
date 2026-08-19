import random


def _java_div(a, b):
    # Truncated (Java-style) integer division: rounds toward zero.
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return q


def _java_mod(a, b):
    # Truncated (Java-style) modulo: result takes the sign of the dividend.
    return a - b * _java_div(a, b)


class Snake:
    class Position:
        __slots__ = ("x", "y")

        def __init__(self, x, y):
            self.x = x
            self.y = y

        def get_x(self):
            return self.x

        def get_y(self):
            return self.y

        def __eq__(self, o):
            if self is o:
                return True
            if o is None or type(o) is not Snake.Position:
                return False
            return self.x == o.x and self.y == o.y

        def __hash__(self):
            return 31 * self.x + self.y

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, food_position):
        self.length = 1
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = [Snake.Position(_java_div(SCREEN_WIDTH, 2), _java_div(SCREEN_HEIGHT, 2))]
        self.score = 0
        self.food_position = food_position
        self._random = random.Random()

    def move(self, direction):
        cur = self.positions[0]
        x = direction.x
        y = direction.y

        new_x = _java_mod(cur.x + (x * self.BLOCK_SIZE), self.SCREEN_WIDTH)
        new_y = _java_mod(cur.y + (y * self.BLOCK_SIZE), self.SCREEN_HEIGHT)

        new_position = Snake.Position(new_x, new_y)

        if new_position == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self):
        while True:
            x = self._random.randrange(_java_div(self.SCREEN_WIDTH, self.BLOCK_SIZE)) * self.BLOCK_SIZE
            y = self._random.randrange(_java_div(self.SCREEN_HEIGHT, self.BLOCK_SIZE)) * self.BLOCK_SIZE
            self.food_position = Snake.Position(x, y)
            if self.food_position not in self.positions:
                break

    def reset(self):
        self.length = 1
        self.positions.clear()
        self.positions.append(Snake.Position(_java_div(self.SCREEN_WIDTH, 2), _java_div(self.SCREEN_HEIGHT, 2)))
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self):
        return self.length

    def get_positions(self):
        return self.positions

    def get_score(self):
        return self.score

    def get_food_position(self):
        return self.food_position