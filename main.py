from FieldManager.FieldManager import FieldManager
import matplotlib.pyplot as plt
import numpy as np
from ConvexHull.ConvexHull import ConvexHull


def read_field(file_name, convex):

    # readfile
    file = open(file_name, 'r')
    size_x = float(file.readline())
    size_y= float(file.readline())
    start = tuple(map(float, file.readline().split(' ')))
    end = tuple(map(float, file.readline().split(' ')))
    ice_num = int(file.readline())

    # read polygons
    for i in range(ice_num):
        iceberg_num = int(file.readline())
        ice_dots = int(file.readline())
        polygon = np.zeros([ice_dots, 2])
        for dot in range(ice_dots):
            polygon[dot, :] = tuple(map(float, file.readline().split(' ')))
        draw_polygon(polygon, iceberg_num, convex)

    file.close()

    return size_x, size_y, start, end, ice_num



def show_field(file_name, convex=False):
    """
    Show field with start, end points and all polygons.
    """

    size_x, size_y, start, end, ice_num = read_field(file_name,convex)

    # figure title
    plt.figure(1, figsize=(5, 5))
    plt.suptitle("Eskimo field", fontsize=15)
    plt.title("Number of icebergs = " + str(ice_num), fontsize=8)

    # plot START + END point
    plt.scatter(start[0], start[1], color="blue", s=10)
    plt.text(start[0] - 8, start[1] + 5, "Start")
    plt.scatter(end[0], end[1], color="red", s=10)
    plt.text(end[0] - 8, end[1] + 5, "End")

    # grid configurations
    plt.xlim(0, size_x)
    plt.ylim(0, size_y)
    plt.legend(loc="best")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
    plt.grid()
    plt.show()


def draw_polygon(polygon, counter, convex):
    """
    draw polygon dots.

    :type polygon: nparray
    :type counter: int
    """
    # Plot the point
    plt.scatter(polygon[:, 0], polygon[:, 1], s=8, label="Polygon" + str(counter))

    # Compute the convex hull of the points
    if convex:
        hull =  ConvexHull(polygon).graham_scan()

        # Plot the convex hull
        plt.plot([p.x for p in hull] + [hull[0].x], [p.y for p in hull] + [hull[0].y], linewidth=1, color='r')

if __name__ == '__main__':
    field = FieldManager(300, (10.0, 10.0), (250.0, 250.0), seed = 80)

    # read file and present the field
    show_field("data_cpp.txt", convex=False)

    # show feild after convex hull
    show_field("data_cpp.txt", convex=True)






