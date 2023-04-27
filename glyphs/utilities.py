from collections import OrderedDict
from operator import itemgetter
import math
import numpy as np


def hexagon_vertices(center, radius, flipped=False):
    vertices = []
    for i in range(6):
        if flipped:
            x = center[0] + radius * math.sin(2 * math.pi * i / 6)
            y = center[1] + radius * math.cos(2 * math.pi * i / 6)
        else:
            x = center[0] + radius * math.cos(2 * math.pi * i / 6)
            y = center[1] + radius * math.sin(2 * math.pi * i / 6)
        vertices.append((x, y))
    return vertices


def compare_points(this_point, comparison_points):
    raw_dict = {point: math.dist(point, this_point) for point in comparison_points}
    return OrderedDict(sorted(raw_dict.items(), key=itemgetter(1)))


def poly_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def convert_to_slope_vector(current_point, next_point):
    return (next_point[0] - current_point[0], next_point[1] - current_point[1])


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):

    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def close_compare(val1, val2):
    for x, y in zip(val1, val2):
        if np.round(x, 3) != np.round(y, 3):
            return False
    return True


def is_parallel_vectors(v1, v2):
    angle = angle_between(v1, v2)
    if np.round(angle, 3) == 0:
        return True
    else:
        return False
def rotate(l, n):
    return l[n:] + l[:n]
