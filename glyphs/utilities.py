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
        vertices.append((np.round(x,4), np.round(y,4)))
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


def total_distance(coords):
    total_dist = 0.0
    prev_x, prev_y = None, None

    for x, y in coords:
        if prev_x is not None and prev_y is not None:
            dist = math.sqrt((x - prev_x)**2 + (y - prev_y)**2)
            total_dist += dist

        prev_x, prev_y = x, y

    return total_dist


def find_repeated_locs(input_list):
    repeated_nums = {}

    for index, num in enumerate(input_list):
        if num in repeated_nums:
            repeated_nums[num].append(index)
        else:
            repeated_nums[num] = [index]

    max_delta = 0
    deltas = {}
    for k,v in repeated_nums.items():
        if len(v)>1:
            delta = v[1]-v[0]
            if delta>max_delta:
                max_delta=delta
                locs = v
    if max_delta == 0:
        locs = [0,len(input_list)]

    return locs


def segments_intersect(seg1, seg2):
    # Calculate the parameters for the intersection of the two lines
    x1, y1 = seg1[0]
    x2, y2 = seg1[1]
    x3, y3 = seg2[0]
    x4, y4 = seg2[1]
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # Lines are parallel
        return False
    t1 = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    t2 = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    # Check if the intersection point is within both line segments
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        return True
    else:
        return False

def check_for_self_intersecting(points):
    n = len(points)
    for i in range(n-1):
        seg1 = (points[i], points[i+1])
        for j in range(i+2, n-1):
            seg2 = (points[j], points[j+1])
            # im not interseted in paths that share points, only crossing
            if len(set([points[j],points[j+1],points[i], points[i+1]])) == 4:
                if segments_intersect(seg1, seg2):
                    return True
    return False
