import constant
import FileHandler.FileHandler as fh
from FieldManager.FieldManager import FieldManager
from GraphCreator.GraphCreator import GraphCreator
import random
import time
from Point.Point import Point
import logging

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
    rand_seed = random.randint(0, 600)
    #rand_seed = 207 #nice example to show
    # rand_seed = 422 example to how to choose random point
    print(rand_seed)
    #rand_seed = 214
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

    '''
    # Step 5 - Create naive Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="naive")
    logging.info("naive length: {}".format(gc.shortest_path()))
    logging.info("naive time: {}".format(time.time() - start_time))
    gc.draw_graph()
    '''

    # Step 6 - Create optimal Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="optimal")
    logging.info("optimal length: {}".format(gc.shortest_path()))
    logging.info("optimal time: {}".format(time.time() - start_time))
    gc.draw_graph()

    '''
    # Step 7 - Create RRT Graph and find the Shortest Path
    start_time = time.time()
    gc.create_graph(graph_type="RRT")
    gc.draw_graph()
    logging.info("RRT length: {}".format(gc.shortest_path()))
    logging.info("RRT time: {}".format(time.time() - start_time))
    gc.draw_graph()
    '''

    # Step 7 - Dubins extension
    gc.dubins_graph(vel=15, phi=17)


if __name__ == "__main__":
    main()
