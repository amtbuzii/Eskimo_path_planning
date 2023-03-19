# Define the Point class

from math import sqrt


class Point:
    def __init__(self, x: float = 0, y: float = 0, x_y: tuple[float, float] = None):
        if x_y is None:
            self.x = x
            self.y = y
        else:
            self.x = x_y[0]
            self.y = x_y[1]

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        elif self.x < other.x:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x} {self.y}"

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def distance(self, other) -> float:
        return round(sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2), 2)

    def check_valid(self, low: float, high: float) -> bool:
        if self.x < low or self.x > high or self.y < low or self.y > high:
            return False
        return True

