import math
import numpy as np
from enum import Enum
from glyphs.utilities import hexagon_vertices, \
    compare_points, convert_to_slope_vector,\
    close_compare, is_parallel_vectors, \
    angle_between, rotate, poly_area, total_distance

ROTATION_MAP = {0: 'ccw',
                1: 'cw'}


def get_current_location(path):
    return np.unravel_index(np.argmax(path, axis=None), path.shape)


def determine_optional_moves(path):
    current_location = get_current_location(path)
    initial_location = tuple(np.argwhere(path == 1)[0])
    size = np.shape(path)[0]
    optional_moves = []
    visted_locs = set(tuple(x) for x in np.argwhere(path != 0))

    for (dx, dy) in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
        px, py = current_location[0] + dx, current_location[1] + dy
        # check to make sure we're on the board
        if px >= 0 and px < size and py >= 0 and py < size:
            # if we're returning home that's ok
            if tuple([px, py]) == initial_location:
                optional_moves.append([px, py])
            else:
                # check to make sure we haven't been there before
                if (px, py) not in visted_locs:
                    optional_moves.append([px, py])

    return optional_moves


class GlyphPath:
    def __init__(self, grid_path, grid_rotations):
        self.grid_path = grid_path
        self.grid_rotations = grid_rotations

        self.path_locations = self._convert_to_locations()
        self.path_rotations = self._convert_to_path_rotations()

    def _convert_to_locations(self):
        x_trace = []
        y_trace = []
        for i in range(int(np.max(self.grid_path))):
            loc = np.argwhere(self.grid_path == i + 1)[0]
            x_trace.append(loc[0] + .5 * loc[1])
            y_trace.append(loc[1] * np.sin(np.deg2rad(60)))

        x_trace.append(x_trace[0])
        y_trace.append(y_trace[0])
        return [(x, y) for x, y in zip(x_trace, y_trace)]

    def _convert_to_path_rotations(self):
        rotations = []
        for i in range(int(np.max(self.grid_path))):
            loc = np.argwhere(self.grid_path == i + 1)[0]
            rotation = ROTATION_MAP[self.grid_rotations[tuple([int(x) for x in loc])]]
            rotations.append(rotation)
        return rotations

    def _add_kernals(self):
        self.kernals = []
        for path_rotation, path_location in zip(self.path_rotations, self.path_locations):
            self.kernals.append(GlyphKernal(path_location, rotation=path_rotation))

    def _follow_path(self):
        all_path_points = []
        # determine first point

        distances = compare_points(self.kernals[1].center_point,
                                   self.kernals[0].shape_points)
        current_point = distances.popitem(last=True)[0]
        self.kernals.append(self.kernals[0])
        for i, kernal in enumerate(self.kernals[:-1]):

            all_path_points.append(current_point)

            target_slope = convert_to_slope_vector(self.kernals[i].center_point,
                                                   self.kernals[i + 1].center_point)

            self.kernals[i].recurse_shape_points(current_point,
                                                 target_slope,
                                                 debug_slopes=False)

            all_path_points.extend(self.kernals[i].subpath)

            same_rotation = self.kernals[i].rotation == self.kernals[i + 1].rotation
            # leap to next kernal

            if i != len(self.kernals) - 1:
                current_point = self.kernals[i + 1].find_point_on_slope(all_path_points[-1], target_slope,
                                                                        same_rotation)

        self.all_path_points = all_path_points
        
        return all_path_points



    def _determine_metrics(self):
        # does it pass
        not_crossing = len(set(self.all_path_points)) ==len(self.all_path_points)

        x,y=tuple(zip(*self.all_path_points))
        area = poly_area(x,y)

        lenght_of_primary_cycle = len(self.path_locations)

        self.metrics = {}
        self.metrics['not_crossing'] = not_crossing
        self.metrics['area'] = area
        self.metrics['concavity'] = area / lenght_of_primary_cycle

        #distance traveled
        self.metrics['distance'] = total_distance(self.path_locations)
        self.metrics['solidity'] = area / self.metrics['distance']

    def run_all(self):
        self._add_kernals()
        self._follow_path()
        self._determine_metrics()
        



class GlyphKernal:
    def __init__(self,
                 center_point,
                 radius=1 / 3,
                 shape='hexagon',
                 rotation='ccw'):
        self.center_point = center_point
        self.shape = shape
        self.radius = radius
        self.anchor_radius = self.compute_anchor_radius(self.radius)
        self.rotation = rotation
        self.add_shape_points()
        self.add_anchor_points()
        self.subpath = []

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
        else:
            shape_points_extended = shape_points_extended

        self.shape_points_extended = shape_points_extended
        for i, point in enumerate(shape_points_extended[:-1]):
            self.shape_points_with_rotation[point] = shape_points_extended[i + 1]

    @staticmethod
    def compute_anchor_radius(radius):
        return 2 * ((radius) ** 2 - (radius / 2) ** 2) ** .5

    def add_anchor_points(self):

        self.anchor_points = []
        if self.shape == 'hexagon':
            self.anchor_points = hexagon_vertices(self.center_point, self.anchor_radius, flipped=True)

        else:
            raise ValueError(f'shape type {self.shape} not yet supported')

        if self.rotation == 'ccw':
            anchor_points = self.anchor_points[::-1]
            anchor_points = rotate(anchor_points, 4)
        else:
            anchor_points = self.anchor_points
            anchor_points = rotate(anchor_points, 2)
        #
        self.anchor_points_with_rotation = {}

        for x, y in zip(self.shape_points_extended[:-1], anchor_points):
            self.anchor_points_with_rotation[x] = (y, y)

        #
        # for i, s in enumerate(self.shape_points[:-1]):
        #     self.anchor_points_with_rotation[s] = (self.anchor_points[i-3],self.anchor_points[i-3])

    def recurse_shape_points(self,
                             point,
                             target_slope,
                             debug_slopes=False):
        """
        during our reverse we want to see
        (1.6666666666666667, 0.5773502691896257) --> (1.5, 0.28867513459481287)
        :param point:
        :param target_slope:
        :param debug_slopes:
        :return:
        (1.6666666666666667, 1.1547005383792515) --> (2.0, 1.1547005383792515)
        shape point position 1
        anchor point position 1
        """

        next_shape_point = self.shape_points_with_rotation[point]
        next_anchor_points = self.anchor_points_with_rotation[point]

        for next_anchor_point in next_anchor_points:
            current_anchor_slope = convert_to_slope_vector(point, next_anchor_point)
            if debug_slopes:
                print(f'Current slope {angle_between(current_anchor_slope, target_slope)}')
            # make a note (1.6666666666666667, 0.5773502691896257) --> (2.0, 0.5773502691896258)

            # check if current slope is is equal to target slope
            if is_parallel_vectors(current_anchor_slope, target_slope):
                self.subpath.append(next_anchor_point)
                return self.subpath

        self.subpath.append(next_shape_point)
        self.recurse_shape_points(next_shape_point, target_slope, debug_slopes=debug_slopes)

    def find_point_on_slope(self,
                            current_point,
                            slope,
                            same_rotation):
        matches = {}
        for point in self.shape_points:
            if is_parallel_vectors(convert_to_slope_vector(current_point, point), slope):
                matches[math.dist(current_point, point)] = point

        if same_rotation:
            return matches[min(matches.keys())]
        else:
            point = matches[min(matches.keys())]

            return self.shape_points_with_rotation[point]


if __name__ == '__main__':
    from glyphs.visualization import render_path_debug, render_path_fill

    """
    Structure of algorithm
    pick random point on first kernal
    cycle in intendended direction
    
    when slope of last lines equeals slope between then we leap
    
    leep to next kernal
    
    
    """
    size = 3
    path = np.zeros((size, size))
    # path[0, 0] = 1
    # path[1, 0] = 2
    # path[1, 1] = 3
    # path[2, 1] = 4
    # path[2, 2] = 5
    # path[1, 2] = 6
    # path[0, 2] = 7
    # path[0, 1] = 8
    rotations = np.zeros((size, size))
    rotations[1, 1] = 1
    rotations[1, 2] = 1
    #
    #
    rotations = np.ones((size, size))
    rotations[1, 1] = 0
    rotations[1, 2] = 0
    path = np.array([[1., 2., 3.],
                     [8., 7., 4.],
                     [0., 6.,5.]])

    glyph_path = GlyphPath(path, rotations)
    glyph_path.run_all()

    print(glyph_path.metrics)
    save_location = 'glyph_figures/debug_fill_path.png'
    render_path_debug(path, glyph_path.all_path_points, save_location)
