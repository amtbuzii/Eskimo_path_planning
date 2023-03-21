# Define the Point class

from math import sqrt
from typing import Union


class Point:
    def __init__(
            self, x: Union[float, tuple[float, float]], y: float = 0):
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

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
