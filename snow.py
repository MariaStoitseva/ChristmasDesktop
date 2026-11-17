import random
import math


class Snowflake:
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(-height, 0)
        self.size = random.uniform(0.8, 2.5)
        self.speed = random.uniform(0.5, 1.8)
        self.phase = random.uniform(0, 6.28)
        self.opacity = random.randint(100, 255)

    def update(self):
        self.y += self.speed
        self.phase += 0.025
        self.x += math.sin(self.phase) * 0.4

    def reset(self, width):
        self.y = -10
        self.x = random.uniform(0, width)


class SnowSurface:
    def __init__(self, x, y, width, max_height=25):
        self.x = x
        self.y = y
        self.width = width
        self.max_height = max_height
        self.segment_width = 5

        count = int(width / self.segment_width) + 1

        self.heights = [0.0] * count

        self.limits = [
            max_height * (
                0.70
                + 0.18 * math.sin(i * 0.15)
                + 0.12 * math.sin(i * 0.43)
            )
            for i in range(count)
        ]

    def get_index(self, x):
        return int((x - self.x) / self.segment_width)

    def collides(self, flake, previous_y):
        if not self.x <= flake.x < self.x + self.width:
            return False

        index = self.get_index(flake.x)
        surface_y = self.y - self.heights[index]

        return previous_y <= surface_y <= flake.y

    def accumulate(self, x):
        index = self.get_index(x)

        for offset in range(-3, 4):
            i = index + offset

            if 0 <= i < len(self.heights):
                amount = 0.9 / (abs(offset) + 1)

                self.heights[i] = min(
                    self.limits[i],
                    self.heights[i] + amount
                )