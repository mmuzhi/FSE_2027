import random
import time

class Snake:
    def __init__(self, screenWidth, screenHeight, blockSize, foodPosition):
        self.length = 1
        self.SCREEN_WIDTH = screenWidth
        self.SCREEN_HEIGHT = screenHeight
        self.BLOCK_SIZE = blockSize
        self.positions = [(screenWidth // 2, screenHeight // 2)]
        self.score = 0
        self.food_position = foodPosition

    def move(self, direction):
        cur = self.positions[0]
        x = direction[0]
        y = direction[1]

        newPosX = (cur[0] + x * self.BLOCK_SIZE) % self.SCREEN_WIDTH
        newPosY = (cur[1] + y * self.BLOCK_SIZE) % self.SCREEN_HEIGHT
        newPos = (newPosX, newPosY)

        if newPos == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and any(newPos == pos for pos in self.positions[2:]):
            self.reset()
        else:
            self.positions.insert(0, newPos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self):
        random.seed(int(time.time()))
        while True:
            x = random.randint(0, (self.SCREEN_WIDTH // self.BLOCK_SIZE) - 1) * self.BLOCK_SIZE
            y = random.randint(0, (self.SCREEN_HEIGHT // self.BLOCK_SIZE) - 1) * self.BLOCK_SIZE
            food_pos = (x, y)
            if food_pos not in self.positions:
                self.food_position = food_pos
                break

    def reset(self):
        self.length = 1
        self.positions = [(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)]
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self):
        return self.length

    def get_positions(self):
        return self.positions.copy()

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