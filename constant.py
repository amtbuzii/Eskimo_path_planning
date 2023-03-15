import numpy as np
import matplotlib.pyplot as plt
from FieldManager.Field import Field

# declare constants

# field parameters
MIN_SIZE = 2
DEAFULT_SEED = 0
DEAFULT_START = (0, 0)
DEAFULT_END = (1, 1)
FILE_PATH = "../Eskimo_path_planning/data_cpp.txt"

# icebergs parameters
MAX_ICEBERGS = 20  # maximum number of icebergs
MIN_DOTS = 3  # min dots in each icebergs
MAX_DOTS = 10  # max dots in each icebergs
MIN_RADIUS = 1  # MIN radius size
MAX_RADIUS = 150  # MAX radius size


# Function

def read_field(file_name):
    """
    read txt file and returns - start, end, polygons
    """

    file = open(file_name, 'r')
    size_x = float(file.readline())
    size_y = float(file.readline())
    start = tuple(map(float, file.readline().split(' ')))
    end = tuple(map(float, file.readline().split(' ')))
    ice_num = int(file.readline())
    polygons = [[] for _ in range(ice_num)]

    # read polygons
    for i in range(ice_num):
        iceberg_num = int(file.readline())
        ice_dots = int(file.readline())
        polygon = np.zeros([ice_dots, 2])
        for dot in range(ice_dots):
            polygon[dot, :] = tuple(map(float, file.readline().split(' ')))
        polygons[i] = polygon
        # draw_polygon(polygon, iceberg_num)

    file.close()

    return Field(start, end, polygons)


def show_field(field_data, convex):
    """
    Show field with start, end points and all polygons.
    """

    # figure title
    # plt.figure(1, figsize=(5, 5))
    plt.suptitle("Eskimo field", fontsize=15)

    # plot START + END point
    plt.scatter(field_data.start[0], field_data.start[1], color="blue", marker="p", s=50, label="Start")
    plt.scatter(field_data.end[0], field_data.end[1], color="red", marker="*", s=50, label="End")

    # Plot polygons:
    for polygon in field_data.polygons:
        # plt.scatter(polygon[:, 0], polygon[:, 1], s=8, label="Polygon" + str(counter))
        p = np.array(polygon)
        plt.scatter(p[:, 0], p[:, 1], s=8)
        if convex:
            plt.plot([p[0] for p in polygon] + [polygon[0][0]], [p[1] for p in polygon] + [polygon[0][1]], linewidth=1)

    # grid configurations
    plt.legend(loc="best")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
    # plt.grid()
    plt.show()
