from Point.Point import Point

# declare constants

# field parameters
MIN_SIZE = 2
DEAFULT_SEED = 0
DEAFULT_START = Point(0.0, 0.0)
DEAFULT_END = Point(1.0, 1.0)
FILE_PATH = "../Eskimo_path_planning/field_data.txt"

# icebergs parameters
MIN_ICEBERGS = 4
MAX_ICEBERGS = 4  # maximum number of icebergs should be 70
MIN_DOTS = 3  # min dots in each icebergs
MAX_DOTS = 10  # max dots in each icebergs
MIN_RADIUS = 90  # MIN radius size
MAX_RADIUS = 100  # MAX radius size - should be 45

# RRT parameters
ITERATION = 500
STEP_SIZE = 4

# Dubins parameters
DUBINS_VEL = 10  # constant velocity
DUBINS_PHI = 50  # maximum allowable roll angle
POLY_TOLERANCE = 5.0
