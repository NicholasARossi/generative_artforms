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

def poly_area(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def generate_slope(current_point, next_point):
    """


    What orientation means
    -1.5 lower left
    -1 keft
    -.5 uper left

    """

    slope =(next_point[1] - current_point[1]) / (next_point[0] - current_point[0])

    is_right = np.sign(np.round(next_point[0],3)-np.round(current_point[0],3))
    is_up = np.sign(np.round(next_point[1],3)-np.round(current_point[1],3))
    return [slope, is_right,is_up]


def close_compare(val1, val2):

    for x,y in zip(val1,val2):
        if np.round(x, 3) != np.round(y, 3):
            return False
    return True
