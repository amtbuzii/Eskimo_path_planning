from Point.Point import Point

# declare constants

# field parameters
MIN_SIZE = 2
DEAFULT_SEED = 0
DEAFULT_START = Point(0.0, 0.0)
DEAFULT_END = Point(1.0, 1.0)
FILE_PATH = "../Eskimo_path_planning/field_data.txt"

# icebergs parameters
MIN_ICEBERGS = 5
MAX_ICEBERGS = 20 # maximum number of icebergs should be 70
MIN_DOTS = 3  # min dots in each icebergs
MAX_DOTS = 10  # max dots in each icebergs
MIN_RADIUS = 30  # MIN radius size
MAX_RADIUS = 50  # MAX radius size - should be 45

#RRT parameters
ITERATION = 2000
STEP_SIZE = 4
