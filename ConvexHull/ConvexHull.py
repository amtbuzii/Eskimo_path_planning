import math
from ConvexHull.Point import Point


def check_input(points):
    if len(points) < 3:  # check validity of the inputs
        raise ValueError('need at least 3 dots')
    for point in points:  # from list of tuple to list op Points
        if len(point) != 2:  # check validity of the inputs
            raise ValueError('need 2 parameters')
        elif not isinstance(point[0], (int, float)) or not isinstance(point[1], (int, float)):
            raise ValueError('only numbers')


# Define the ConvexHull Class

class ConvexHull:
    def __init__(self, points):
        check_input(points)  # check input
        self.points = []
        for point in points:  # from list of tuple to list op Points

            self.points.append(Point(point[0], point[1]))
        self.hull = self.graham_scan()

    def graham_scan(self):
        """
        Returns the vertices of the convex hull of a set of points using the Graham scan algorithm
        """
        # Find the point with the lowest y-coordinate (min function implemented in Point Class
        pivot = min(self.points)

        # Sort the points in increasing order of the angle they and the pivot point make with the x-axis
        sorted_points = sorted(self.points, key=lambda p: (
            math.atan2(p.y - pivot.y, p.x - pivot.x), (p.x - pivot.x) ** 2 + (p.y - pivot.y) ** 2))

        # Add the first two sorted points to the convex hull
        hull = [pivot, sorted_points[0]]
        for i in range(1, len(sorted_points)):
            while len(hull) >= 2 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
                hull.pop()
            hull.append(sorted_points[i])

        # convert to list of tuple [(x,y),(x,y),(x,y)...]
        hull = [(p.x, p.y) for p in hull]

        # special case - all vertex on the same line - the convexHull is only 2 point - add 3rd point
        if len(hull) == 2:
            hull.append(hull[1])

        return hull


def orientation(p, q, r):
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
