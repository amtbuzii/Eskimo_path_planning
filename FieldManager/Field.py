from Point.Point import Point


class Field:
    def __init__(self, size: float, start: Point, end: Point, polygons: list[list]):
        self.size = size
        self.start = start
        self.end = end
        self.polygons = polygons
