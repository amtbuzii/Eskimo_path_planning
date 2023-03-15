from FieldManager.FieldManager import FieldManager
import matplotlib.pyplot as plt
import numpy as np
from ConvexHull.ConvexHull import ConvexHull
from ConvexHull.Point import Point
from GraphCreator.GraphCreator import GraphCreator
from constant import *
from FieldManager.Field import Field


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
    plt.figure(1, figsize=(5, 5))
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
    plt.grid()
    plt.show()




if __name__ == '__main__':
    '''
    seed option to show:
    - 80
    - 9
    - 90
    - 199
    '''

    # Step 1: Field parameters
    start_point = (10.0, 10.0)
    end_point = (250.0, 250.0)
    field_size = 300
    rand_seed = 80

    # Step 2: Start the program - create the field and write to file
    field = FieldManager(size=field_size, start=start_point, end=end_point, seed=rand_seed)

    # Step 3: Read from file and show the field - need to be correct.....
    test_field = read_field(FILE_PATH)
    show_field(test_field, convex=False)

    # Step 4 - Convex Hull
    test_field.polygons = field.get_convexhull_polygons()
    show_field(test_field, convex=True)

    # Step 5 - Create  naive Graph (naive and optimal)
    gc = GraphCreator(test_field)
    gc.naive_graph()
    gc.draw_graph()

    # Step 6 - Create  naive Graph (naive and optimal)
    gc = GraphCreator(test_field)
    gc.optimal_graph()
    gc.draw_graph()

    # Step 7 - Find the Shortest Path
    pass

    # Step 8 - Dubbins extension
    pass
