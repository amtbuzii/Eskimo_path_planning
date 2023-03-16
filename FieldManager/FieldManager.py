import random
import numpy as np
import math
from ConvexHull.ConvexHull import ConvexHull
from constant import *

def write_to_file(lines=''):
    """
    write the data to file.
    :type lines: string
    """

    try:
        with open(FILE_PATH, "w") as file:
            file.writelines(lines)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: You don't have the required permissions to access the file.")
    except OSError as e:
        print("Error: An operating system error occurred -", e)
    except ValueError:
        print("Error: Invalid value or format.")
    except TypeError:
        print("Error: Invalid data type.")
    except Exception as e:
        print("Error: An unexpected error occurred -", e)
    else:
        print("The data was successfully written to the file.")


def random_point(x_center, y_center, radius, dots):
    """
    generate random points for each polygon. (using rejection sampling method - 78.5% success)

    :type x_center: int
    :type y_center: int
    :type radius: int
    :type dots: int
    :rtype: nparray[n, (x,y)]
    """
    rnd_points = np.zeros([dots, 2])

    for i in range(dots):
        while True:
            x = random.random() * radius * 2 - radius
            y = random.random() * radius * 2 - radius
            if x * x + y * y < (radius * radius):  # check correctness of the coordinate
                rnd_points[i, :] = x_center + x, y_center + y
                break

    return rnd_points


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class FieldManager:
    def __init__(self, size=MIN_SIZE, start=DEAFULT_START, end=DEAFULT_END, seed=DEAFULT_SEED):
        """
        initialize the object parameters. write to file and draw the field

        :type size: int
        :type start: tuple
        :type end: tuple
        :type seed: int
        :rtype: List[int]
        """
        random.seed(seed)
        if size <= 0:
            raise ValueError('field size must be greater than 0')
        self._size = size

        if not self._check_input(start) or not self._check_input(end):
            raise ValueError('invalid coordinate')

        self._start = start
        self._end = end
        self._ice_num = random.randint(1, MAX_ICEBERGS)
        self._polygons = [[] for _ in range(self._ice_num)]
        self._convex_hull_polygons = [[] for _ in range(self._ice_num)]

        polygons_text = self._create_polygons()  # write the polygons to string and show them in plot

        self._convex_hull()

        # write the header text
        start = " ".join([str(_) for _ in self._start])
        end = " ".join([str(_) for _ in self._end])
        header_text = f"{self._size}\n{self._size}\n{start}\n{end}\n{self._ice_num}"

        # write to file
        write_to_file(lines=header_text + polygons_text)

    def _check_input(self, coordinate):
        # check start point
        x = coordinate[0]
        y = coordinate[1]
        if x < 0 or x > self._size or y < 0 or y > self._size:
            return False
        return True

    def _create_polygons(self):
        """
        create random polygons (icebergs)
        :rtype: string
        """
        polygons_text = ''

        for counter in range(self._ice_num):
            # random center coordinate
            temp_x = random.randint(0, self._size)
            temp_y = random.randint(0, self._size)

            # Checking the proper distance between the center point and the start and end points
            center_start_distance = distance(self._start[0], self._start[1], temp_x, temp_y)
            center_end_distance = distance(self._end[0], self._end[1], temp_x, temp_y)
            _radius = min(MAX_RADIUS, min(center_start_distance, center_end_distance))

            # random radius
            temp_radius = random.randint(MIN_RADIUS, int(_radius))

            # random number of dots in the iceberg, (min 3)
            temp_dots = random.randint(MIN_DOTS, MAX_DOTS)

            # get random dots using random_point function
            temp_rnd_point = random_point(x_center=temp_x, y_center=temp_y, radius=temp_radius,
                                          dots=temp_dots)  # random dots coordinate

            # checking that all point in the field (0 to size) - if not fix (0 or size)
            for dot in temp_rnd_point:
                dot[0] = min(dot[0], self._size-1)
                dot[1] = min(dot[1], self._size-1)
                dot[0] = max(dot[0], 0)
                dot[1] = max(dot[1], 0)
                self._polygons[counter].append(tuple(dot))

            # add to polygons text
            points = "\n".join([" ".join(item) for item in temp_rnd_point.astype(str)])
            polygons_text += f"\n{counter + 1}\n{temp_dots}\n{points}"

        return polygons_text

    def _convex_hull(self):
        for polygon in range(self._ice_num):
            self._convex_hull_polygons[polygon] = ConvexHull(self._polygons[polygon]).hull

    def get_field(self):
        return self._size, self._size, self._start, self._end, self._ice_num, self._polygons, self._convex_hull_polygons

    def get_convexhull_polygons(self):
        return self._convex_hull_polygons
