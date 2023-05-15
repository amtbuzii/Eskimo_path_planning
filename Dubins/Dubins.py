from typing import Union
import math
import numpy as np
from enum import Enum
import copy
import constant


class TurnType(Enum):
    LSL = 1
    LSR = 2
    RSL = 3
    RSR = 4
    RLR = 5
    LRL = 6


class Waypoint:
    def __init__(self, x: float, y: float, psi: int) -> None:
        self.x = x
        self.y = y
        self.psi = psi

    def __str__(self) -> str:
        return "x: " + str(self.x) + ", y: " + str(self.y) + ", psi: " + str(self.psi)


class Param:
    def __init__(self, p_init: Waypoint, seg_final: list[float], turn_radius: float) -> None:
        self.p_init = p_init
        self.seg_final = seg_final
        self.turn_radius = turn_radius
        self.type = 0

    def __str__(self) -> str:
        return "p_init: " + str(self.p_init) + ", seg_final: " + str(self.seg_final) + ", turn_radius: " + str(
            self.turn_radius) + ", type: " + str(self.type)


def wrapTo360(angle: float) -> float:
    # replace angle 0 to 360
    posIn = angle > 0
    angle = angle % 360
    if angle == 0 and posIn:
        angle = 360
    return angle


def wrap_to_180(angle: float) -> float:
    q = (angle < -180) or (180 < angle)
    if (q):
        angle = wrapTo360(angle + 180) - 180
    return angle


def heading_to_standard(hdg: float) -> float:
    # Convert NED heading to standard unit circle...
    thet = wrapTo360(90 - wrap_to_180(hdg))
    return thet


def calc_dubins_path(wpt1: Waypoint, wpt2: Waypoint, vel: float, phi_lim: float) -> dict[
    Union[int, tuple[Union[int, float], ...]], Param]:
    # Calculate a dubins path between two waypoints
    param = Param(p_init=wpt1, seg_final=[0, 0, 0], turn_radius=0)

    tz = [0, 0, 0, 0, 0, 0]
    pz = [0, 0, 0, 0, 0, 0]
    qz = [0, 0, 0, 0, 0, 0]

    # Convert the headings from NED to standard unit circle, and then to radians
    psi1 = heading_to_standard(wpt1.psi) * math.pi / 180
    psi2 = heading_to_standard(wpt2.psi) * math.pi / 180

    # Do math
    param.turn_radius = (vel * vel) / (9.8 * math.tan(phi_lim * math.pi / 180))
    dx = wpt2.x - wpt1.x
    dy = wpt2.y - wpt1.y
    D = math.sqrt(dx * dx + dy * dy)
    d = D / param.turn_radius  # Normalize by turn radius...makes length calculation easier down the road.

    # Angles defined in the paper
    theta = math.atan2(dy, dx) % (2 * math.pi)
    alpha = (psi1 - theta) % (2 * math.pi)
    beta = (psi2 - theta) % (2 * math.pi)
    best_word = -1
    best_cost = -1

    # Calculate all dubins paths between points
    tz[0], pz[0], qz[0] = dubins_LSL(alpha, beta, d)
    tz[1], pz[1], qz[1] = dubins_LSR(alpha, beta, d)
    tz[2], pz[2], qz[2] = dubins_RSL(alpha, beta, d)
    tz[3], pz[3], qz[3] = dubins_RSR(alpha, beta, d)
    tz[4], pz[4], qz[4] = dubins_RLR(alpha, beta, d)
    tz[5], pz[5], qz[5] = dubins_LRL(alpha, beta, d)

    param_dict = dict()
    # Now, pick the one with the lowest cost
    for x in range(6):
        if (tz[x] != -1):
            cost = tz[x] + pz[x] + qz[x]
            param.seg_final = [tz[x], pz[x], qz[x]]
            param.type = TurnType(x + 1)
            param_dict[cost] = copy.deepcopy(param)

    return param_dict


# Here's all of the dubins path math
def dubins_LSL(alpha: float, beta: float, d: float) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    tmp0 = d + math.sin(alpha) - math.sin(beta)
    tmp1 = math.atan2((math.cos(beta) - math.cos(alpha)), tmp0)
    p_squared = 2 + d * d - (2 * math.cos(alpha - beta)) + (2 * d * (math.sin(alpha) - math.sin(beta)))
    if p_squared < 0:
        # print('No LSL Path')
        p = -1
        q = -1
        t = -1
    else:
        t = (tmp1 - alpha) % (2 * math.pi)
        p = math.sqrt(p_squared)
        q = (beta - tmp1) % (2 * math.pi)
    return t, p, q


def dubins_RSR(alpha: float, beta: float, d: float) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    tmp0 = d - math.sin(alpha) + math.sin(beta)
    tmp1 = math.atan2((math.cos(alpha) - math.cos(beta)), tmp0)
    p_squared = 2 + d * d - (2 * math.cos(alpha - beta)) + 2 * d * (math.sin(beta) - math.sin(alpha))
    if p_squared < 0:
        # print('No RSR Path')
        p = -1
        q = -1
        t = -1
    else:
        t = (alpha - tmp1) % (2 * math.pi)
        p = math.sqrt(p_squared)
        q = (-1 * beta + tmp1) % (2 * math.pi)
    return t, p, q


def dubins_RSL(alpha: float, beta: float, d: float) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    tmp0 = d - math.sin(alpha) - math.sin(beta)
    p_squared = -2 + d * d + 2 * math.cos(alpha - beta) - 2 * d * (math.sin(alpha) + math.sin(beta))
    if p_squared < 0:
        # print('No RSL Path')
        p = -1
        q = -1
        t = -1
    else:
        p = math.sqrt(p_squared)
        tmp2 = math.atan2((math.cos(alpha) + math.cos(beta)), tmp0) - math.atan2(2, p)
        t = (alpha - tmp2) % (2 * math.pi)
        q = (beta - tmp2) % (2 * math.pi)
    return t, p, q


def dubins_LSR(alpha: float, beta: float, d: float) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    tmp0 = d + math.sin(alpha) + math.sin(beta)
    p_squared = -2 + d * d + 2 * math.cos(alpha - beta) + 2 * d * (math.sin(alpha) + math.sin(beta))
    if p_squared < 0:
        # print('No LSR Path')
        p = -1
        q = -1
        t = -1
    else:
        p = math.sqrt(p_squared)
        tmp2 = math.atan2((-1 * math.cos(alpha) - math.cos(beta)), tmp0) - math.atan2(-2, p)
        t = (tmp2 - alpha) % (2 * math.pi)
        q = (tmp2 - beta) % (2 * math.pi)
    return t, p, q


def dubins_RLR(alpha: float, beta: float, d: float) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    tmp_rlr = (6 - d * d + 2 * math.cos(alpha - beta) + 2 * d * (math.sin(alpha) - math.sin(beta))) / 8
    if abs(tmp_rlr) > 1:
        # print('No RLR Path')
        p = -1
        q = -1
        t = -1
    else:
        p = (2 * math.pi - math.acos(tmp_rlr)) % (2 * math.pi)
        t = (alpha - math.atan2((math.cos(alpha) - math.cos(beta)), d - math.sin(alpha) + math.sin(beta)) + p / 2 % (
                2 * math.pi)) % (2 * math.pi)
        q = (alpha - beta - t + (p % (2 * math.pi))) % (2 * math.pi)

    return t, p, q


def dubins_LRL(alpha: float, beta: float, d: float) -> tuple[Union[int, float], Union[int, float], Union[int, float]]:
    tmp_lrl = (6 - d * d + 2 * math.cos(alpha - beta) + 2 * d * (-1 * math.sin(alpha) + math.sin(beta))) / 8
    if abs(tmp_lrl) > 1:
        # print('No LRL Path')
        p = -1
        q = -1
        t = -1
    else:
        p = (2 * math.pi - math.acos(tmp_lrl)) % (2 * math.pi)
        t = (-1 * alpha - math.atan2((math.cos(alpha) - math.cos(beta)),
                                     d + math.sin(alpha) - math.sin(beta)) + p / 2) % (2 * math.pi)
        q = ((beta % (2 * math.pi)) - alpha - t + (p % (2 * math.pi))) % (2 * math.pi)
    return t, p, q


def dubins_traj(param: Param, step: float) -> np.ndarray:
    # Build the trajectory from the lowest-cost path
    x = 0
    i = 0
    length = (param.seg_final[0] + param.seg_final[1] + param.seg_final[2]) * param.turn_radius
    length = math.floor(length / step)
    path = -1 * np.ones((length, 3))

    while x < length:
        path[i] = dubins_path(param, x)
        x += step
        i += 1
    return path


def dubins_path(param: Param, t: int) -> np.ndarray[float]:
    # Helper function for curve generation
    tprime = t / param.turn_radius
    p_init = np.array([0, 0, heading_to_standard(param.p_init.psi) * math.pi / 180])
    #
    L_SEG = 1
    S_SEG = 2
    R_SEG = 3
    DIRDATA = np.array([[L_SEG, S_SEG, L_SEG], [L_SEG, S_SEG, R_SEG], [R_SEG, S_SEG, L_SEG], [R_SEG, S_SEG, R_SEG],
                        [R_SEG, L_SEG, R_SEG], [L_SEG, R_SEG, L_SEG]])
    #
    types = DIRDATA[param.type.value - 1][:]
    param1 = param.seg_final[0]
    param2 = param.seg_final[1]
    mid_pt1 = dubins_segment(param1, p_init, types[0])
    mid_pt2 = dubins_segment(param2, mid_pt1, types[1])

    if (tprime < param1):
        end_pt = dubins_segment(tprime, p_init, types[0])
    elif (tprime < (param1 + param2)):
        end_pt = dubins_segment(tprime - param1, mid_pt1, types[1])
    else:
        end_pt = dubins_segment(tprime - param1 - param2, mid_pt2, types[2])

    end_pt[0] = end_pt[0] * param.turn_radius + param.p_init.x
    end_pt[1] = end_pt[1] * param.turn_radius + param.p_init.y
    end_pt[2] = end_pt[2] % (2 * math.pi)
    return end_pt


def dubins_segment(seg_param, seg_init, seg_type):
    # Helper function for curve generation
    L_SEG = 1
    S_SEG = 2
    R_SEG = 3
    seg_end = np.array([0.0, 0.0, 0.0])
    if (seg_type == L_SEG):
        seg_end[0] = seg_init[0] + math.sin(seg_init[2] + seg_param) - math.sin(seg_init[2])
        seg_end[1] = seg_init[1] - math.cos(seg_init[2] + seg_param) + math.cos(seg_init[2])
        seg_end[2] = seg_init[2] + seg_param
    elif (seg_type == R_SEG):
        seg_end[0] = seg_init[0] - math.sin(seg_init[2] - seg_param) + math.sin(seg_init[2])
        seg_end[1] = seg_init[1] + math.cos(seg_init[2] - seg_param) - math.cos(seg_init[2])
        seg_end[2] = seg_init[2] - seg_param
    elif (seg_type == S_SEG):
        seg_end[0] = seg_init[0] + math.cos(seg_init[2]) * seg_param
        seg_end[1] = seg_init[1] + math.sin(seg_init[2]) * seg_param
        seg_end[2] = seg_init[2]

    return seg_end


def angle_between_points(pt_a, pt_b):
    # Calculate the differences between the x and y coordinates of the two points
    dx = pt_b[0] - pt_a[0]
    dy = pt_b[1] - pt_a[1]

    # Calculate the angle between the two points using the arctangent function
    angle = math.atan2(dy, dx)

    # Convert the angle to degrees and return it
    return math.degrees(angle)
