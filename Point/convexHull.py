'''
import math
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class ConvexHull:
    def __init__(self, points):
        self.points = points
        self.hull = self.graham_scan()

    def graham_scan(self):
        # Find the point with the lowest y-coordinate
        lowest_point = min(self.points, key=lambda point: point.y)
        print("lowes", lowest_point)

        # Sort the remaining points by their polar angle with respect to the lowest point
        sorted_points = sorted(self.points, key=lambda point: (math.atan2(point.y - lowest_point.y, point.x - lowest_point.x), point.x))

        # Initialize the stack with the first two points
        stack = [sorted_points[0], sorted_points[1]]

        # Iterate over the remaining points, adding them to the stack if they turn left
        for point in sorted_points[2:]:
            while len(stack) >= 2 and self.orientation(stack[-2], stack[-1], point) <= 0:
                stack.pop()
            stack.append(point)

        return stack

    @staticmethod
    def orientation(p1, p2, p3):
        return (p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y)

    def plot(self):
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]

        plt.plot(x, y, 'bo')
        for i in range(len(self.hull)):
            plt.plot([self.hull[i].x, self.hull[(i+1) % len(self.hull)].x],
                     [self.hull[i].y, self.hull[(i+1) % len(self.hull)].y],
                     'r-', lw=2)

        plt.show()




points = [Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1), Point(3, 0), Point(0, 0),Point(3, 3),Point(2, -1), Point(2, -4), Point(1, -3)]
convex_hull = ConvexHull(points)
print(convex_hull.hull)
convex_hull.plot()
'''


import math
import matplotlib.pyplot as plt

# Define the Point class and the graham_scan() function

class Point:
    def __init__(self, x, y):
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
        return f"({self.x}, {self.y})"

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

def graham_scan(points):
    """Returns the vertices of the convex hull of a set of points using the Graham scan algorithm"""
    # Find the point with the lowest y-coordinate
    pivot = min(points)

    # Sort the points in increasing order of the angle they and the pivot point make with the x-axis
    sorted_points = sorted(points, key=lambda p: (math.atan2(p.y-pivot.y, p.x-pivot.x), (p.x-pivot.x)**2 + (p.y-pivot.y)**2))

    # Add the first two sorted points to the convex hull
    hull = [pivot, sorted_points[0]]
    for i in range(1, len(sorted_points)):
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
            hull.pop()
        hull.append(sorted_points[i])

    return hull


points = [Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1), Point(3, 0), Point(0, 0),Point(3, 3),Point(2, -1), Point(2, -4), Point(1, -3)]


# Compute the convex hull of the points
hull = graham_scan(points)

# Plot the points and the convex hull
fig, ax = plt.subplots()
ax.scatter([p.x for p in points], [p.y for p in points], color='b', label='Points')
ax.plot([p.x for p in hull]+[hull[0].x], [p.y for p in hull]+[hull[0].y], color='r', label='Convex Hull')
ax.legend()
plt.show()
