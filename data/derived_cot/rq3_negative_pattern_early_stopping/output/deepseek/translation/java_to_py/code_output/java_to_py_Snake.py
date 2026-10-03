import random

class Snake:
    class Position:
        def __init__(self, x, y):
            self._x = x
            self._y = y

        def getX(self):
            return self._x

        def getY(self):
            return self._y

        def __eq__(self, other):
            if not isinstance(other, Snake.Position):
                return False
            return self._x == other._x and self._y == other._y

        def __hash__(self):
            return 31 * self._x + self._y

        def __repr__(self):
            return f"Position({self._x},{self._y})"

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, foodPosition):
        self.length = 1
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = [self.Position(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.score = 0
        self.foodPosition = foodPosition
        self.random = random.Random()

    def move(self, direction):
        cur = self.positions[0]
        x = direction.getX()
        y = direction.getY()

        newX = (cur.getX() + (x * self.BLOCK_SIZE)) % self.SCREEN_WIDTH
        newY = (cur.getY() + (y * self.BLOCK_SIZE)) % self.SCREEN_HEIGHT

        newPosition = self.Position(newX, newY)

        if newPosition == self.foodPosition:
            self.eatFood()

        if len(self.positions) > 2 and newPosition in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, newPosition)
            if len(self.positions) > self.length:
                self.positions.pop()

    def randomFoodPosition(self):
        while True:
            x = self.random.randrange(self.SCREEN_WIDTH // self.BLOCK_SIZE) * self.BLOCK_SIZE
            y = self.random.randrange(self.SCREEN_HEIGHT // self.BLOCK_SIZE) * self.BLOCK_SIZE
            self.foodPosition = self.Position(x, y)
            if self.foodPosition not in self.positions:
                break

    def reset(self):
        self.length = 1
        self.positions.clear()
        self.positions.append(self.Position(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.score = 0
        self.randomFoodPosition()

    def eatFood(self):
        self.length += 1
        self.score += 100
        self.randomFoodPosition()

    def getLength(self):
        return self.length

    def getPositions(self):
        return self.positions

    def getScore(self):
        return self.score

    def getFoodPosition(self):
        return self.foodPosition