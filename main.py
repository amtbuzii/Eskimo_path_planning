from constant import *
from FieldManager.FieldManager import FieldManager
from GraphCreator.GraphCreator import GraphCreator
import random
import time

def random_point(size):
    _x = random.randint(0, size)
    _y = random.randint(0, size)
    return (_x, _y)


def main():
    '''
       seed option to show:
       MAX_RADIUS = 150  # MAX radius size

       - 80 - to movie
       - 9
       - 90
       - 199 - special case
       - 50 nice
       - 95 BUG NEED TO UNDERSTAND

       MAX_RADIUS = 30  # MAX radius size
       '''

    # Step 1: Field parameters
    field_size = random.randint(100, 600)
    # field_size = 192
    # start_point = random_point(field_size)
    # end_point = random_point(field_size)
    start_point = (5, 5)
    end_point = (field_size - 10, field_size - 10)
    rand_seed = 99

    # Step 2: Start the program - create the field and write to file
    field_m = FieldManager(size=field_size, start=start_point, end=end_point, seed=rand_seed)

    # Step 3: Read from file and show the field - need to be correct.....
    test_field = read_field(FILE_PATH)
    show_field(test_field, convex=False)

    # Step 4 - Convex Hull
    test_field.polygons = field_m.get_convexhull_polygons()
    show_field(test_field, convex=True)

    # Step 5 - Create naive Graph
    gc = GraphCreator(test_field)
    start_time = time.time()
    gc.create_graph(type="naive")
    print("naive length: ", gc.shortest_path())
    print("naive time: ", time.time() - start_time)
    gc.draw_graph()

    # Step 6 - Create optimal Graph
    start_time = time.time()
    gc.create_graph(type="optimal")

    # Step 7 - Find the Shortest Path
    print("optimal length: ", gc.shortest_path())
    print("optimal time: ", time.time() - start_time)
    gc.draw_graph()

    # Step 8 - Dubins extension
    pass


if __name__ == '__main__':
    main()


'''
 frames = []
    for t in range(14):
        image = imageio.v2.imread(f'./img/img_{t}.png')
        frames.append(image)
    imageio.mimsave('./example.gif',  # output gif
                    frames,  # array of input frames
                    fps=5)  # optional: frames per second
'''
