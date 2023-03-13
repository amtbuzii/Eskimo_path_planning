from ConvexHull.Point import Point

def test_eq():
    # test the == operator
    p1 = Point(0, 1)
    p2 = Point(0, 1)
    assert (p1 == p2) == True


def test_lt():
    # test the > operator

    p1 = Point(1, 1)
    p2 = Point(0, 0)
    assert (p1 > p2) == True


def test_gt():
    # test the < operator
    p1 = Point(1, 1)
    p2 = Point(0, 0)
    assert (p1 < p2) == False


def test_print():
    # test the print operator
    p1 = Point(0, 1)
    assert (p1.__str__()) == "(0, 1)"
