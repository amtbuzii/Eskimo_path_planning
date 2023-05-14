import logging
import random
import numpy as np
import math
from ConvexHull.ConvexHull import ConvexHull
import constant
from Point.Point import Point
import FileHandler.FileHandler as fh
from FieldManager.Field import Field
import logging


class FieldManager:
    def __init__(
        self,
        size: int = constant.MIN_SIZE,
        start: Point = constant.DEAFULT_START,
        end: Point = constant.DEAFULT_END,
        seed: int = constant.DEAFULT_SEED,
    ):
        """
        initialize the object parameters. write to file and draw the field
        """
        random.seed(seed)

        if size <= 0:
            logging.warning("field size must be greater than 2")
            raise ValueError("field size must be greater than 2")

        self._size = size
        self._start = start
        self._end = end

        if not self._start.check_valid(0, self._size) or not self._end.check_valid(0, self._size):
            logging.warning("invalid coordinate")
            raise ValueError("invalid coordinate")

        self._ice_num = random.randint(constant.MIN_ICEBERGS, constant.MAX_ICEBERGS)
        self._polygons = (
            self._create_polygons()
        )  # write the polygons to string and show them in plot
        self._convex_hull = self._convex_hull()

        self.field_parameters = Field(
            size=self._size, start=self._start, end=self._end, polygons=self._polygons
        )
        fh.create_file(self.field_parameters)

    def _create_polygons(self) -> list[list]:
        """
        create random polygons (icebergs)
        """
        polygons = [[] for _ in range(self._ice_num-7)]

        for polygon in range(self._ice_num-7):
            # random center coordinate
            temp_point = Point(
                random.randint(0, self._size), random.randint(0, self._size)
            )

            # Checking the proper distance between the center point and the start and end points
            center_start_distance = self._start.distance(temp_point)
            center_end_distance = self._end.distance(temp_point)
            _radius = min(
                constant.MAX_RADIUS,
                min(center_start_distance, center_end_distance),
            )

            # random radius
            temp_radius = random.randint(
                min(constant.MIN_RADIUS, int(_radius)), int(_radius)
            )

            # random number of dots in the iceberg, (min 3)
            temp_dots = random.randint(constant.MIN_DOTS, constant.MAX_DOTS)

            # get random dots using random_point function
            temp_rnd_point = self._random_points(
                center_point=temp_point, radius=temp_radius, dots=temp_dots
            )  # random dots coordinate
            polygons[polygon] = temp_rnd_point


        p1 = [Point(20, 0), Point(40, 0), Point(20, 290), Point(40, 290)]
        p2 = [Point(60, 10), Point(80, 10), Point(60, 300), Point(80, 300)]
        p3 = [Point(100, 0), Point(120, 0), Point(100, 290), Point(120, 290)]
        p4 = [Point(140, 10), Point(160, 10), Point(140, 300), Point(160, 300)]
        p5 = [Point(180, 0), Point(200, 0), Point(180, 290), Point(200, 290)]
        p6 = [Point(220, 10), Point(240, 10), Point(220, 300), Point(240, 300)]
        p7 = [Point(260, 0), Point(280, 0), Point(260, 290), Point(280, 290)]
        #p8 = [Point(280, 10), Point(160, 10), Point(140, 300), Point(160, 300)]

        polygons.append(p1)
        polygons.append(p2)
        polygons.append(p3)
        polygons.append(p4)
        polygons.append(p5)
        polygons.append(p6)
        polygons.append(p7)
        #polygons.append(p8)



        return polygons

    def _random_points(
        self, center_point: Point, radius: float, dots: int
    ) -> list[Point]:
        """
        generate random points for each polygon. (using rejection sampling method - 78.5% success)
        """

        rnd_points = []

        for i in range(dots):
            while True:
                _x = random.random() * radius * 2 - radius
                _y = random.random() * radius * 2 - radius
                if _x * _x + _y * _y < (radius * radius):  # check correctness of the coordinate
                    _x = min(center_point.x + _x, self._size - 1)
                    _y = min(center_point.y + _y, self._size - 1)
                    rnd_points.append(Point(_x, _y))
                    break
        return rnd_points

    def _convex_hull(self) -> list[list]:
        ch_polygons = [[] for _ in range(self._ice_num)]
        for polygon in range(self._ice_num):
            ch_polygons[polygon] = ConvexHull(self._polygons[polygon]).hull
        return ch_polygons

    def get_convexhull_polygons(self) -> list[list]:
        return self._convex_hull
