from constant import *
from FieldManager.FieldManager import FieldManager
from GraphCreator.GraphCreator import GraphCreator

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
