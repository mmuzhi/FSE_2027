import random


def _java_mod(a, b):
    r = a % b
    if r != 0 and a < 0:
        r -= b
    return r


class Snake:
    class Position:
        __slots__ = ('_x', '_y')

        def __init__(self, x, y):
            self._x = x
            self._y = y

        def __setattr__(self, name, value):
            if hasattr(self, name):
                raise AttributeError("Position is immutable")
            super().__setattr__(name, value)

        def getX(self):
            return self._x

        def getY(self):
            return self._y

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return self._x == other._x and self._y == other._y

        def equals(self, other):
            return self.__eq__(other)

        def hashCode(self):
            return 31 * self._x + self._y

        __hash__ = hashCode

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, foodPosition):
        self._SCREEN_WIDTH = SCREEN_WIDTH
        self._SCREEN_HEIGHT = SCREEN_HEIGHT
        self._BLOCK_SIZE = BLOCK_SIZE
        self._length = 1
        self._positions = []
        self._positions.append(Snake.Position(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self._score = 0
        self._foodPosition = foodPosition
        self._random = random.Random()

    @property
    def SCREEN_WIDTH(self):
        return self._SCREEN_WIDTH

    @property
    def SCREEN_HEIGHT(self):
        return self._SCREEN_HEIGHT

    @property
    def BLOCK_SIZE(self):
        return self._BLOCK_SIZE

    def move(self, direction):
        cur = self._positions[0]
        x = direction.getX()
        y = direction.getY()

        newX = _java_mod(cur.getX() + (x * self.BLOCK_SIZE), self.SCREEN_WIDTH)
        newY = _java_mod(cur.getY() + (y * self.BLOCK_SIZE), self.SCREEN_HEIGHT)

        newPosition = Snake.Position(newX, newY)

        if newPosition == self._foodPosition:
            self.eatFood()

        if len(self._positions) > 2 and newPosition in self._positions[2:]:
            self.reset()
        else:
            self._positions.insert(0, newPosition)
            if len(self._positions) > self._length:
                self._positions.pop()

    def randomFoodPosition(self):
        while True:
            x = self._random.randrange(self.SCREEN_WIDTH // self.BLOCK_SIZE) * self.BLOCK_SIZE
            y = self._random.randrange(self.SCREEN_HEIGHT // self.BLOCK_SIZE) * self.BLOCK_SIZE
            self._foodPosition = Snake.Position(x, y)
            if self._foodPosition not in self._positions:
                break

    def reset(self):
        self._length = 1
        self._positions.clear()
        self._positions.append(Snake.Position(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self._score = 0
        self.randomFoodPosition()

    def eatFood(self):
        self._length += 1
        self._score += 100
        self.randomFoodPosition()

    def getLength(self):
        return self._length

    def getPositions(self):
        return self._positions

    def getScore(self):
        return self._score

    def getFoodPosition(self):
        return self._foodPosition