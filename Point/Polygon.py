"""
New data structure - for circular linked list
"""

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw_next = None         # Holds the adjacent point in the clockwise direction
        self.ccw_next = None        # Holds the adjacent point in the counter clockwise direction.

    def __sub__(self, other):
        """
        subtract  2 points .
        :param p: Point
        :return: Point
        """
        return Node(self.x - other.x, self.y - other.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        """
        Cheack if 2 points are equal.

        :param p: Point
        :return: Boolean
        """
        return self.x == other.x and self.y == other.y


def merge(convex1, convex2):
    """
    Merge 2 circular linked list (convex) to one.

    :param convex1: Point
    :param convex1: Point
    :return: Boolean    :
    """
    # get the rightmost point of left convex hull
    p = max(chull1, key=lambda point: point.x)

    # get the leftmost poitn of right convex hull
    q = min(chull2, key=lambda point: point.x)

    # make copies of p and q
    cp_p = p
    cp_q = q

    # raise the bridge pq to the uper tangent
    prev_p = None
    prev_q = None
    while (True):
        prev_p = p
        prev_q = q
        if q.cw_next:
            # move p clockwise as long as it makes left turn
            while direction(p, q, q.cw_next) < 0:
                q = q.cw_next
        if p.ccw_next:
            # move p as long as it makes right turn
            while direction(q, p, p.ccw_next) > 0:
                p = p.ccw_next

        if p == prev_p and q == prev_q:
            break

    # lower the bridge cp_p cp_q to the lower tangent
    prev_p = None
    prev_q = None
    while (True):
        prev_p = cp_p
        prev_q = cp_q
        if cp_q.ccw_next:
            # move q as long as it makes right turn
            while direction(cp_p, cp_q, cp_q.ccw_next) > 0:
                cp_q = cp_q.ccw_next
        if cp_p.cw_next:
            # move p as long as it makes left turn
            while direction(cp_q, cp_p, cp_p.cw_next) < 0:
                cp_p = cp_p.cw_next
        if cp_p == prev_p and cp_q == prev_q:
            break

    # remove all other points
    p.cw_next = q
    q.ccw_next = p

    cp_p.ccw_next = cp_q
    cp_q.cw_next = cp_p

    # final result
    result = []
    start = p
    while (True):
        result.append(p)
        p = p.ccw_next

        if p == start:
            break

    return result

