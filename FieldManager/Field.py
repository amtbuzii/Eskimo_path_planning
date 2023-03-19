from Point.Point import Point
from dataclasses import dataclass


@dataclass()
class Field:
    size: float
    start: Point
    end: Point
    polygons: list[list]
