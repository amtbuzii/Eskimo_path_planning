import math
from Point.Point import (
    Point,
)
import logging


# Define the ConvexHull Class


class ConvexHull:
    def __init__(
        self,
        points: list[Point],
    ):
        self.points = points
        self.check_input()
        self.hull = self.graham_scan()

    def check_input(
        self,
    ) -> None:
        if len(self.points) < 3:  # check validity of the inputs
            logging.warning("need at least 3 dots")
            raise ValueError("need at least 3 dots")

    def graham_scan(
        self,
    ) -> list[Point]:
        """
        Returns the vertices of the convex hull of a set of points using the Graham scan algorithm
        """
        # Find the point with the lowest y-coordinate (min function implemented in Point Class
        pivot = min(self.points)

        # Sort the points in increasing order of the angle they and the pivot point make with the x-axis
        sorted_points = sorted(
            self.points,
            key=lambda p: (
                math.atan2(
                    p.y - pivot.y,
                    p.x - pivot.x,
                ),
                (p.x - pivot.x) ** 2 + (p.y - pivot.y) ** 2,
            ),
        )

        # Add the first two sorted points to the convex hull
        hull = [
            pivot,
            sorted_points[0],
        ]
        for i in range(
            1,
            len(sorted_points),
        ):
            while (
                len(hull) >= 2
                and orientation(
                    hull[-2],
                    hull[-1],
                    sorted_points[i],
                )
                != 2
            ):
                hull.pop()
            hull.append(sorted_points[i])

        # special case - all vertex on the same line.
        # the convexHull is only 2 point - add 3rd point
        if len(hull) == 2:
            hull.append(hull[1])

        return hull


def orientation(
    p: Point,
    q: Point,
    r: Point,
) -> int:
    """
    Returns the orientation of the triplet (p, q, r)
       0 --> p, q and r are colinear
       1 --> Clockwise
       2 --> Counterclockwise
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # colinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise
