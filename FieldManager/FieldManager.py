import random
import numpy as np
import matplotlib.pyplot as plt
import math


def write_to_file(lines=''):
    """
    write the data to file.
    :type lines: string
    """

    try:
        with open("../Eskimo_path_planning/data_cpp.txt", "w") as file:
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
    def __init__(self, size=2, start=(0, 0), end=(1, 1), seed=0):
        """
        initialize the object parameters. write to file and draw the field

        :type size: int
        :type start: tuple
        :type end: tuple
        :type seed: int
        :rtype: List[int]
        """
        random.seed(seed)

        self._size = size
        if not self._check_input(start) or not self._check_input(end):
            print("invalid coordinate")
            return
        self._start = start
        self._end = end
        self._ice_num = random.randint(1, 20)  # max 19 icebergs
        polygons_text = self._create_polygons()  # write the polygons to string and show them in plot

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
            min_radius = min(30, min(center_start_distance, center_end_distance))

            # random radius
            temp_radius = random.randint(1, int(min_radius))

            # random number of dots in the iceberg, (min 3)
            temp_dots = random.randint(3, 10)

            # get random dots using random_point function
            temp_rnd_point = random_point(x_center=temp_x, y_center=temp_y, radius=temp_radius,
                                          dots=temp_dots)  # random dots coordinate

            # checking that all point in the file (0 to size)
            for dot in temp_rnd_point:
                dot[0] = min(dot[0], self._size-1)
                dot[1] = min(dot[1], self._size-1)
                dot[0] = max(dot[0], 0)
                dot[1] = max(dot[1], 0)

            # add to polygons text
            points = "\n".join([" ".join(item) for item in temp_rnd_point.astype(str)])
            polygons_text += f"\n{counter + 1}\n{temp_dots}\n{points}"

        return polygons_text





'''
    @staticmethod
    def _draw_polygon(polygon, counter):
        """
        draw polygon dots.

        :type polygon: nparray
        :type counter: int
        """

        plt.scatter(polygon[:, 0], polygon[:, 1], s=8, label="Polygon" + str(counter))

    def show_field(self):
        """
        Show field with start, end points and all polygons.
        """

        # figure title
        plt.figure(1, figsize=(5, 5))
        plt.suptitle("FieldManager field", fontsize=15)
        plt.title("Number of icebergs = " + str(self._ice_num), fontsize=8)

        # plot START + END point
        plt.scatter(self._start[0], self._start[1], color="blue", s=10)
        plt.text(self._start[0] - 8, self._start[1] + 5, "Start")
        plt.scatter(self._end[0], self._end[1], color="red", s=10)
        plt.text(self._end[0] - 8, self._end[1] + 5, "End")

        # grid configurations
        plt.xlim(0, self._size)
        plt.ylim(0, self._size)
        plt.legend(loc="best")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
        plt.grid()

        plt.show()
'''