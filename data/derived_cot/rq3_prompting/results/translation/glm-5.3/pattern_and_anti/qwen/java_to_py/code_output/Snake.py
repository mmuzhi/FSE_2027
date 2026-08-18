import random


def _java_div(a: int, b: int) -> int:
    """Java int division: truncates toward zero."""
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _java_mod(a: int, b: int) -> int:
    """Java int remainder: takes the sign of the dividend (unlike Python's %)."""
    r = abs(a) % abs(b)
    return -r if a < 0 else r


class Position:
    __slots__ = ("_x", "_y")

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) is not type(other):  # mirrors getClass() != o.getClass()
            return False
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return 31 * self._x + self._y


class Snake:
    def __init__(self, screen_width: int, screen_height: int, block_size: int, food_position: Position):
        self.length = 1
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.BLOCK_SIZE = block_size
        self.positions = [Position(_java_div(self.SCREEN_WIDTH, 2), _java_div(self.SCREEN_HEIGHT, 2))]
        self.score = 0
        self.food_position = food_position
        self._random = random.Random()

    def move(self, direction: Position) -> None:
        cur = self.positions[0]
        x = direction.get_x()
        y = direction.get_y()

        new_x = _java_mod(cur.get_x() + x * self.BLOCK_SIZE, self.SCREEN_WIDTH)
        new_y = _java_mod(cur.get_y() + y * self.BLOCK_SIZE, self.SCREEN_HEIGHT)

        new_position = Position(new_x, new_y)

        if new_position == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self) -> None:
        while True:  # do...while
            x = self._random.randrange(_java_div(self.SCREEN_WIDTH, self.BLOCK_SIZE)) * self.BLOCK_SIZE
            y = self._random.randrange(_java_div(self.SCREEN_HEIGHT, self.BLOCK_SIZE)) * self.BLOCK_SIZE
            self.food_position = Position(x, y)
            if self.food_position not in self.positions:
                break

    def reset(self) -> None:
        self.length = 1
        self.positions.clear()
        self.positions.append(Position(_java_div(self.SCREEN_WIDTH, 2), _java_div(self.SCREEN_HEIGHT, 2)))
        self.score = 0
        self.random_food_position()

    def eat_food(self) -> None:
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self) -> int:
        return self.length

    def get_positions(self) -> list:
        return self.positions

    def get_score(self) -> int:
        return self.score

    def get_food_position(self) -> Position:
        return self.food_position