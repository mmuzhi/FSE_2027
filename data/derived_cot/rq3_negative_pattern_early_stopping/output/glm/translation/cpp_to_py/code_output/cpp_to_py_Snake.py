import random
import time
from typing import List, Tuple

def _cpp_div(a: int, b: int) -> int:
    q = a // b
    if (a ^ b) < 0 and q * b != a:
        q += 1
    return q

def _cpp_mod(a: int, b: int) -> int:
    return a - _cpp_div(a, b) * b

class Snake:
    def __init__(self, screen_width: int, screen_height: int, block_size: int, food_position: Tuple[int, int]):
        self.length = 1
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.BLOCK_SIZE = block_size
        self.score = 0
        self.food_position = food_position
        self.positions: List[Tuple[int, int]] = [(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)]

    def move(self, direction: Tuple[int, int]) -> None:
        cur = self.positions[0]
        x, y = direction

        new_pos = (
            _cpp_mod(cur[0] + x * self.BLOCK_SIZE, self.SCREEN_WIDTH),
            _cpp_mod(cur[1] + y * self.BLOCK_SIZE, self.SCREEN_HEIGHT)
        )

        if new_pos == self.food_position:
            self.eat_food()

        if len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def random_food_position(self) -> None:
        random.seed(int(time.time()))
        while True:
            self.food_position = (
                random.randrange(self.SCREEN_WIDTH // self.BLOCK_SIZE) * self.BLOCK_SIZE,
                random.randrange(self.SCREEN_HEIGHT // self.BLOCK_SIZE) * self.BLOCK_SIZE
            )
            if self.food_position not in self.positions:
                break

    def reset(self) -> None:
        self.length = 1
        self.positions = [(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)]
        self.score = 0
        self.random_food_position()

    def eat_food(self) -> None:
        self.length += 1
        self.score += 100
        self.random_food_position()

    def get_length(self) -> int:
        return self.length

    def get_positions(self) -> List[Tuple[int, int]]:
        return self.positions.copy()

    def get_score(self) -> int:
        return self.score

    def get_food_position(self) -> Tuple[int, int]:
        return self.food_position

    def get_SCREEN_WIDTH(self) -> int:
        return self.SCREEN_WIDTH

    def get_SCREEN_HEIGHT(self) -> int:
        return self.SCREEN_HEIGHT

    def get_BLOCK_SIZE(self) -> int:
        return self.BLOCK_SIZE