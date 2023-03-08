import random
import numpy as np
import matplotlib.pyplot as plt


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
        self._start = start
        self._end = end
        self._ice_num = random.randint(1, 5)  # max 19 icebergs

        # write the header text
        start = " ".join([str(_) for _ in self._start])
        end = " ".join([str(_) for _ in self._end])
        header_text = "%s \n%s \n%s \n%s \n%s" % (self._size, self._size, start, end, self._ice_num)

        # write the polygons text
        polygons_text = self._get_random_points()

        write_to_file(lines=header_text + polygons_text)



    def _get_random_points(self):
        """
        generate random icebergs (using rejection_sampling function)
        :rtype: string
        """
        polygons_text = ''

        for counter in range(self._ice_num):
            temp_x = random.randint(0, self._size)  # random x coordinate
            temp_y = random.randint(0, self._size)  # random y coordinate
            temp_radios = random.randint(1, 20)  # random radios
            temp_n = random.randint(3, 6)  # random number of dots in the iceberg
            temp_rnd_point = self._random_point(temp_x, temp_y, temp_radios, temp_n)  # random dots coordinate

            # add to polygons text
            points = "\n".join([" ".join(item) for item in temp_rnd_point.astype(str)])
            polygons_text += "\n%s \n%s \n%s " % (counter+1, temp_n, points)

            # draw the polygon
            self._draw_polygon(temp_rnd_point, counter+1)

        return polygons_text

    def _random_point(self, x_center, y_center, radios, n):
        """
        generate random point for polygon. (using rejection_sampling function)

        :type x_center: int
        :type y_center: int
        :type radios: int
        :type n: int - number of icebergs
        :rtype: nparray[n, (x,y)]
        """
        rnd_points = np.zeros([n, 2])

        for i in range(n):
            rnd_points[i, :] = self._rejection_sampling(radios, x_center, y_center)

        return rnd_points

    @staticmethod
    def _rejection_sampling(radios, x_center, y_center):
        """
        randomize point and check if the point inside the radios. (78.5% success)

        :type radios: int
        :type x_center: int
        :type y_center: int
        :rtype: tuple(x,y)
        """
        while True:
            x = random.random() * radios * 2 - radios
            y = random.random() * radios * 2 - radios
            if x * x + y * y < (radios * radios):  # check correctness of the coordinate
                return x_center + x, y_center + y

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
