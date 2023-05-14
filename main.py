import constant
import FileHandler.FileHandler as fh
from FieldManager.FieldManager import FieldManager
from GraphCreator.GraphCreator import GraphCreator
import random
import time
from Point.Point import Point
import logging
import numpy as np


logging.basicConfig(
    filename="test.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def main():

    # Step 1: Field parameters
    field_size = 300
    start_point = Point(5, 5)
    end_point = Point(field_size - 10,  10)
    rand_seed = random.randint(0, 600)
    rand_seed = 168

    # Step 2: Start the program - create the field and write to file
    field_m = FieldManager(
        size=field_size, start=start_point, end=end_point, seed=rand_seed
    )
    logging.info("Field FieldManager success")
    logging.info("Field seed: {}".format(rand_seed))
    logging.info("Field size: {}".format(field_size))

    # Step 3: Read from file and show the field
    test_field = fh.read_field(constant.FILE_PATH)
    #fh.show_field(test_field, convex=False)

    # Step 4 - Convex Hull
    test_field.polygons = field_m.get_convexhull_polygons()
    #fh.show_field(test_field, convex=True)

    gc = GraphCreator(test_field)

    # Step 5 - Create naive Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="naive")
    naive_length = gc.shortest_path()
    naive_runtime = time.time() - start_time
    logging.info("naive length: {}".format(naive_length))
    logging.info("naive time: {}".format(naive_runtime))
    gc.draw_graph()

    # Step 6 - Create optimal Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="optimal")
    optimal_length = gc.shortest_path()
    optimal_runtime = time.time() - start_time
    logging.info("optimal length: {}".format(optimal_length))
    logging.info("optimal time: {}".format(optimal_runtime))
    gc.draw_graph()

    # Step 7 - Create RRT Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="RRT")
    random_length = gc.shortest_path()
    random_runtime = time.time() - start_time
    logging.info("RRT length: {}".format(random_length))
    logging.info("RRT time: {}".format(random_runtime))
    gc.draw_graph()

    # Step 8 - Dubins extension
    #gc.create_graph(graph_type="optimal")
    #gc.shortest_path()
    #gc.dubins_graph(vel=10, phi=17)
    


if __name__ == "__main__":
    main()
