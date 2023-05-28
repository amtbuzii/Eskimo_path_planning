import constant
import FileHandler.FileHandler as fh
from FieldManager.FieldManager import FieldManager
from GraphCreator.GraphCreator import GraphCreator
import random
import time
from Point.Point import Point
import logging
import matplotlib.pyplot as plt

logging.basicConfig(
    filename="test.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def main():
    # Step 1: Field parameters
    field_size = 300
    start_point = Point(5, 5)
    end_point = Point(field_size - 10, field_size - 10)
    rand_seed = random.randint(0, 500)

    # Step 2: Start the program - create the field and write to file
    field_m = FieldManager(
        size=field_size, start=start_point, end=end_point, seed=rand_seed
    )
    logging.info("Field FieldManager success")
    logging.info("Field seed: {}".format(rand_seed))
    logging.info("Field size: {}".format(field_size))

    # Step 3: Read from file and show the field
    test_field = fh.read_field(constant.FILE_PATH)
    fh.show_field(test_field, convex=False)
    plt.show()

    # Step 4 - Convex Hull
    test_field.polygons = field_m.get_convexhull_polygons()
    fh.show_field(test_field, convex=True)
    plt.show()

    gc = GraphCreator(test_field)

    # Step 5 - Create naive Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="Naive")
    naive_length = gc.shortest_path()
    naive_runtime = time.time() - start_time
    logging.info("naive length: {}".format(naive_length))
    logging.info("naive time: {}".format(naive_runtime))
    gc.draw_graph()
    plt.show()

    # Step 6 - Create optimal Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="Optimal")
    optimal_length = gc.shortest_path()
    optimal_runtime = time.time() - start_time
    logging.info("optimal length: {}".format(optimal_length))
    logging.info("optimal time: {}".format(optimal_runtime))
    gc.draw_graph()
    plt.show()

    # Step 7 - Create optimal* Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="Greedy")
    greedy_length = gc.shortest_path()
    greedy_runtime = time.time() - start_time
    logging.info("greedy length: {}".format(greedy_length))
    logging.info("greedy time: {}".format(greedy_runtime))
    gc.draw_graph()
    plt.show()

    # Step 8 - Create RRT Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="RRT")
    random_length = gc.shortest_path()
    random_runtime = time.time() - start_time
    logging.info("RRT length: {}".format(random_length))
    logging.info("RRT time: {}".format(random_runtime))
    gc.draw_graph()
    plt.show()

    # Step 9 - Dubins extension
    start_time = time.time()
    gc.create_graph(graph_type="Dubins")
    dubins_length = gc.get_dubins_path_length()
    dubins_runtime = time.time() - start_time
    logging.info("Dubins length: {}".format(dubins_length))
    logging.info("Dubins time: {}".format(dubins_runtime))
    gc.draw_graph()
    plt.show()

    return


if __name__ == "__main__":
    main()
