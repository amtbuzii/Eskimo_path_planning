import math
from Point import Point
import matplotlib.pyplot as plt


# Define the ConvexHull Class


class ConvexHull:
    def __init__(self, points):
        self.points = points
        self.hull = self.graham_scan()

    def graham_scan(self):
        """Returns the vertices of the convex hull of a set of points using the Graham scan algorithm"""
        # Find the point with the lowest y-coordinate
        pivot = min(self.points)

        # Sort the points in increasing order of the angle they and the pivot point make with the x-axis
        sorted_points = sorted(points, key=lambda p: (math.atan2(p.y-pivot.y, p.x-pivot.x), (p.x-pivot.x)**2 + (p.y-pivot.y)**2))

        # Add the first two sorted points to the convex hull
        hull = [pivot, sorted_points[0]]
        for i in range(1, len(sorted_points)):
            while len(hull) >= 2 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
                hull.pop()
            hull.append(sorted_points[i])
        return hull


def orientation(p, q, r):
    """Returns the orientation of the triplet (p, q, r)
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


points = [Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1), Point(3, 0), Point(0, 0),Point(3, 3),Point(2, -1), Point(2, -4), Point(1, -3)]
ch = ConvexHull(points)


# Compute the convex hull of the points
hull = ch.graham_scan()

for i in hull:
    print(i)
# Plot the points and the convex hull
fig, ax = plt.subplots()
ax.scatter([p.x for p in points], [p.y for p in points], color='b', label='Points')
ax.plot([p.x for p in hull]+[hull[0].x], [p.y for p in hull]+[hull[0].y], color='r', label='Convex Hull')
ax.legend()
plt.show()


