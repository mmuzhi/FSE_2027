import random
import time


def _c_div(a, b):
    # C++-style integer division (truncates toward zero)
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _c_mod(a, b):
    # C++-style modulo (result takes the sign of the dividend)
    return a - _c_div(a, b) * b


class Snake:
    def __init__(self, screenWidth, screenHeight, blockSize, foodPosition):
        self.length = 1
        self.SCREEN_WIDTH = screenWidth
        self.SCREEN_HEIGHT = screenHeight
        self.BLOCK_SIZE = blockSize
        self.score = 0
        self.food_position = (foodPosition[0], foodPosition[1])
        self.positions = [(_c_div(self.SCREEN_WIDTH, 2), _c_div(self.SCREEN_HEIGHT, 2))]

    def move(self, direction):
        cur = self.positions[0]
        x = direction[0]
        y = direction[1]

        new_pos = (
            _c_mod(cur[0] + x * self.BLOCK_SIZE, self.SCREEN_WIDTH),
            _c_mod(cur[1] + y * self.BLOCK_SIZE, self.SCREEN_HEIGHT),
        )

        if new_pos == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self):
        random.seed(int(time.time()))
        while True:
            self.food_position = (
                random.randrange(_c_div(self.SCREEN_WIDTH, self.BLOCK_SIZE)) * self.BLOCK_SIZE,
                random.randrange(_c_div(self.SCREEN_HEIGHT, self.BLOCK_SIZE)) * self.BLOCK_SIZE,
            )
            if self.food_position not in self.positions:
                break

    def reset(self):
        self.length = 1
        self.positions = [(_c_div(self.SCREEN_WIDTH, 2), _c_div(self.SCREEN_HEIGHT, 2))]
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self):
        return self.length

    def get_positions(self):
        return list(self.positions)

    def get_score(self):
        return self.score

    def get_food_position(self):
        return self.food_position

    def get_SCREEN_WIDTH(self):
        return self.SCREEN_WIDTH

    def get_SCREEN_HEIGHT(self):
        return self.SCREEN_HEIGHT

    def get_BLOCK_SIZE(self):
        return self.BLOCK_SIZE