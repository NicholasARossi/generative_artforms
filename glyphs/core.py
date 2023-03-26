import math
import numpy as np
from collections import OrderedDict
from operator import itemgetter

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

def return_closest_point():
    pass

def compare_points(this_point, comparison_points):
    raw_dict = { point: math.dist(point,this_point)   for point in comparison_points }
    return OrderedDict(sorted(raw_dict.items(), key=itemgetter(1)))



class GlyphPath:
    def __init__(self, grid_path):
        self.grid_path = grid_path
        self.path_locations = self.convert_to_locations()

    def convert_to_locations(self):
        x_trace = []
        y_trace = []
        for i in range(int(np.max(self.grid_path))):
            loc = np.argwhere(self.grid_path == i + 1)[0]
            x_trace.append(loc[0] + .5 * loc[1])
            y_trace.append(loc[1] * np.sin(np.deg2rad(60)))

        x_trace.append(x_trace[0])
        y_trace.append(y_trace[0])
        return [(x, y) for x, y in zip(x_trace, y_trace)]

    def add_kernals(self):
        self.kernals = []
        for path_location in self.path_locations:
            self.kernals.append(GlyphKernal(path_location))

    def follow_path(self):
        all_path_points = []
        # determine first point

        distances = compare_points(self.kernals[1].center_point,
                       self.kernals[0].shape_points)
        current_point = distances.popitem(last=True)[0]
        all_path_points.append(current_point)

        for i, kernal in enumerate(self.kernals[:-1]):


            # check if same roation
            if self.kernals[i].rotation == self.kernals[i+1].rotation:
                self.kernals[i].shape_points_with_rotation[current_point]

            else:
                pass

            # else:
            #     # determine anchor options
            #     anchor_distances = compare_points(self.kernals[i + 1].center_point,
            #                                       self.kernals[i].anchor_points)
            #     anchor1, anchor2 = anchor_distances.popitem(last=False), anchor_distances.popitem(last=False)
            #
            # pass


        # v1 = next(iter(anchor_distances))

        #what is the equadistant anchor point

        # self.kernals[0].shape_points.remove(first_point)
        # for kernal in self.kernals

        # all_path_points.append(distances[max(distances)])



class GlyphKernal:
    def __init__(self,
                 center_point,
                 radius=1 / 3,
                 shape='hexagon',
                 rotation='cw'):
        self.center_point = center_point
        self.shape = shape
        self.radius = radius
        self.anchor_radius = self.compute_anchor_radius(self.radius)
        self.rotation = rotation
        self.add_shape_points()
        self.add_anchor_points()

    def add_shape_points(self):
        self.shape_points = []
        if self.shape == 'hexagon':
            self.shape_points = hexagon_vertices(self.center_point, self.radius)

        else:
            raise ValueError(f'shape type {self.shape} not yet supported')

        shape_points_extended = self.shape_points
        shape_points_extended.append(self.shape_points[0])

        self.shape_points_with_rotation = {}
        if self.rotation == 'cw':
            shape_points_extended = shape_points_extended[::-1]

        for i,point in enumerate(shape_points_extended[:-1]):
            self.shape_points_with_rotation[point] = shape_points_extended[i+1]


    @staticmethod
    def compute_anchor_radius(radius):
        return 2 * ((radius) ** 2 - (radius / 2) ** 2) ** .5

    def add_anchor_points(self):

        self.anchor_points = []
        if self.shape == 'hexagon':
            self.anchor_points = hexagon_vertices(self.center_point, self.anchor_radius, flipped=True)

        else:
            raise ValueError(f'shape type {self.shape} not yet supported')

    def recurse_shape_points(self, point, current_slope=None):
        next_point = self.shape_points_with_rotation[point]
        curent_slope = (point[0] -next_point[0])/(point[1] -next_point[1])

