from Point.Point import Point

# declare constants

# field parameters
MIN_SIZE = 2
DEFAULT_SEED = 0
DEFAULT_START = Point(0.0, 0.0)
DEFAULT_END = Point(10.0, 10.0)
FILE_PATH = "../Eskimo_path_planning/field_data.txt"
FIELD_SIZE = 300

# icebergs parameters
MIN_ICEBERGS = 5
MAX_ICEBERGS = 9  # maximum number of icebergs should be 70
MIN_DOTS = 3  # min dots in each icebergs
MAX_DOTS = 10  # max dots in each icebergs
MIN_RADIUS = 60  # MIN radius size
MAX_RADIUS = 80  # MAX radius size - should be 45

# RRT parameters
ITERATION = 500
STEP_SIZE = 4

# Dubins parameters
DUBINS_VEL = 13  # constant velocity
DUBINS_PHI = 45  # maximum allowable roll angle
POLY_TOLERANCE = 5
