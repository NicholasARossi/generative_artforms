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


class GlyphKernal:
    def __init__(self,
                 center_point,
                 radius=1 / 3,
                 shape='hexagon'):
        self.center_point = center_point
        self.shape = shape
        self.radius = radius
        self.anchor_radius = self.compute_anchor_radius(self.radius)
        self.add_shape_points()
        self.add_anchor_points()

    def add_shape_points(self):
        self.shape_points = []
        if self.shape == 'hexagon':
            self.shape_points = hexagon_vertices(self.center_point, self.radius)

        else:
            raise ValueError(f'shape type {self.shape} not yet supported')

    @staticmethod
    def compute_anchor_radius(radius):
        return 2 * ((radius) ** 2 - (radius / 2) ** 2) ** .5

    def add_anchor_points(self):

        self.anchor_points = []
        if self.shape == 'hexagon':
            self.anchor_points = hexagon_vertices(self.center_point, self.anchor_radius, flipped=True)

        else:
            raise ValueError(f'shape type {self.shape} not yet supported')
