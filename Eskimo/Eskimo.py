import random
import numpy as np
import matplotlib.pyplot as plt


def write_to_file(header=False, lines=''):
    """
    write the data to file.
    :type header: boolean
    :type lines: string
    """

    try:
        if header:
            with open("../data_cpp.txt", "w") as file:
                file.writelines(lines)
        else:
            with open("../data_cpp.txt", "a") as file:
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


class Eskimo:
    def __init__(self, size=2, start=(0, 0), end=(1, 1)):
        """
        initialize the object parameters. write to file and draw the field

        :type size: int
        :type start: tuple
        :type end: tuple
        :rtype: List[int]
        """

        self._size = size
        self._start = start
        self._end = end
        self._ice_num = random.randint(1, 5)  # max 19 icebergs
        start = " ".join([str(_) for _ in self._start])
        end = " ".join([str(_) for _ in self._end])
        # write header to file
        header_text = "%s \n%s \n%s \n%s \n%s \n" % (self._size, self._size, start, end, self._ice_num)
        write_to_file(header=True, lines=header_text)

        # generate random icebergs
        for c in range(self._ice_num):
            temp_x = random.randint(0, size)            # random x coordinate
            temp_y = random.randint(0, size)            # random y coordinate
            temp_radios = random.randint(1, 20)         # random radios
            temp_n = random.randint(3, 6)               # random number of dots in the iceberg
            temp_rnd_point = self.random_point(temp_x, temp_y, temp_radios, temp_n)     # random dots coordinate

            # write polygon to file
            points = "\n".join([" ".join(item) for item in temp_rnd_point.astype(str)])
            polygon_text = "%s \n%s \n%s " % (c+1, temp_n, points)
            write_to_file(header =False, lines=polygon_text)

            # draw the polygon
            self.draw_field(temp_rnd_point, c+1)

        # present the all field
        self.show_field()

    def random_point(self, x_center, y_center, radios, n):
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
            rnd_points[i, :] = self.rejection_sampling(radios, x_center, y_center)

        return rnd_points

    @staticmethod
    def rejection_sampling(radios, x_center, y_center):
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
            if x * x + y * y < (radios * radios):   # check correctness of the coordinate
                return x_center + x, y_center + y

    @staticmethod
    def draw_field(polygon, counter):
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

        plt.figure(1, figsize=(5, 5))
        plt.suptitle("Eskimo field", fontsize=15)
        plt.title("Number of ices = "+str(self._ice_num), fontsize=8)
        plt.scatter(self._start[0], self._start[1], color="blue", s=10)
        plt.text(self._start[0]-8, self._start[1]+5, "Start")
        plt.scatter(self._end[0], self._end[1], color="red", s=10)
        plt.text(self._end[0]-8, self._end[1]+5, "End")
        plt.xlim(0, self._size)
        plt.ylim(0, self._size)
        plt.legend(loc="best")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
        plt.grid()
        plt.show()

