import random

class Solution:

    def __init__(self, radius: float, x_center: float, y_center: float):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center
        self.x = x_center
        self.y = y_center

    def randPoint(self) -> List[float]:
        while True:
            x = random.uniform(self.x - self.radius, self.x + self.radius)
            y = random.uniform(self.y - self.radius, self.y + self.radius)
            if (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2:
                return [x, y]