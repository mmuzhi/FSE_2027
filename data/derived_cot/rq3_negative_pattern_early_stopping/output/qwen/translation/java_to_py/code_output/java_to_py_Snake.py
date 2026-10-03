import random

class Snake:
    class Position:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def __eq__(self, other):
            if isinstance(other, Snake.Position):
                return self.x == other.x and self.y == other.y
            return False
        
        def __hash__(self):
            return hash((self.x, self.y))
        
        def get_x(self):
            return self.x
        
        def get_y(self):
            return self.y

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, food_position):
        self.length = 1
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BLOCK_SIZE = BLOCK_SIZE
        self.positions = []
        self.positions.append(Snake.Position(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.score = 0
        self.food_position = food_position
        self.random = random.Random()

    def move(self, direction):
        cur = self.positions[0]
        x, y = direction.get_x(), direction.get_y()
        new_x = (cur.x + x * self.BLOCK_SIZE) % self.SCREEN_WIDTH
        new_y = (cur.y + y * self.BLOCK_SIZE) % self.SCREEN_HEIGHT
        new_position = Snake.Position(new_x, new_y)

        if new_position == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and any(new_position == pos for pos in self.positions[2:]):
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self):
        while True:
            x = random.randint(0, (self.SCREEN_WIDTH // self.BLOCK_SIZE) - 1) * self.BLOCK_SIZE
            y = random.randint(0, (self.SCREEN_HEIGHT // self.BLOCK_SIZE) - 1) * self.BLOCK_SIZE
            new_food = Snake.Position(x, y)
            if new_food not in self.positions:
                self.food_position = new_food
                break

    def reset(self):
        self.length = 1
        self.positions = [Snake.Position(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)]
        self.score = 0
        self.random_food_position()

    def eat_food(self):
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self):
        return self.length

    def get_positions(self):
        return self.positions.copy()  # Return a copy to prevent mutation

    def get_score(self):
        return self.score

    def get_food_position(self):
        return self.food_position