import math
import numpy as np
import pandas as pd
from glyphs.utilities import hexagon_vertices, \
    compare_points, convert_to_slope_vector, \
    close_compare, is_parallel_vectors, \
    angle_between, rotate, poly_area, total_distance, find_repeated_locs, check_for_self_intersecting
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

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


class GridExplorer:
    def __init__(self, size):
        self.all_paths = []
        self.spawning_locations = []
        self.size = size
        self._initialize_spawn_locations()

    def _initialize_spawn_locations(self):

        for x_loc in range(self.size):
            for y_loc in range(self.size):
                spawing_location = np.zeros((self.size, self.size))
                spawing_location[x_loc, y_loc] = 1
                self.spawning_locations.append(spawing_location)

    def _move(self, path):
        """
        Recursively explore the grid to find all closed cycles
        """
        optional_moves = determine_optional_moves(path)
        for optional_move in optional_moves:
            if tuple(optional_move) == tuple(np.argwhere(path == 1)[0]):
                self.all_paths.append(path)
            else:
                # move to the location and recurse
                new_path = path.copy()
                new_path[optional_move[0], optional_move[1]] = np.max(new_path) + 1
                self._move(new_path)

    def explore_closed_cylces(self):
        for spawning_location in tqdm(self.spawning_locations):
            self._move(spawning_location)

    def save_cycles_to_csv(self, save_location=None):
        # dedup all paths
        df = pd.DataFrame({'raw_paths': self.all_paths})
        logger.info(f'total number of unique skeletons prior to dedup {len(df)}')

        df['path_tuples'] = df['raw_paths'].apply(lambda x: tuple((x != 0).ravel()))
        # dedup by path hash
        df_dedup = df.drop_duplicates(subset=['path_tuples'])
        logger.info(f'total number of unique skeletons post dedup {len(df_dedup)}')
        self.all_paths = df_dedup['raw_paths'].values.tolist()
        if save_location:
            df_dedup.to_csv(save_location)


class GlyphPath:
    def __init__(self, grid_path, grid_rotations):
        self.grid_path = grid_path
        self.grid_rotations = grid_rotations

        self.path_locations = self._convert_to_locations()
        self.path_rotations = self._convert_to_path_rotations()
        self.metrics = None

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
        self.kernals.append(self.kernals[1])
        for i, kernal in enumerate(self.kernals[:-1]):
            all_path_points.append(current_point)

            target_slope = convert_to_slope_vector(self.kernals[i].center_point,
                                                   self.kernals[i + 1].center_point)

            self.kernals[i].recurse_shape_points(current_point,
                                                 target_slope,
                                                 debug_slopes=False)

            if len(self.kernals) > 2 and i >= len(self.kernals) - 2:
                subpath = [item for item in self.kernals[i].subpath if item not in all_path_points]
            else:
                subpath = self.kernals[i].subpath

            all_path_points.extend(subpath)

            # boundaries = find_repeated_locs(all_path_points)
            #
            # all_path_points = all_path_points[boundaries[0]:boundaries[1]]
            # leap to next kernal

            same_rotation = self.kernals[i].rotation == self.kernals[i + 1].rotation
            current_point = self.kernals[i + 1].find_point_on_slope(all_path_points[-1], target_slope,
                                                                    same_rotation)

        # trim off little bits

        linked_dict = {all_path_points[i]: all_path_points[i + 1] if i < len(all_path_points) - 1 else None for i in
                       range(len(all_path_points))}

        # # #
        # # # # recurse dict to clip nubs
        # #
        def recurse_dict(key):
            if key in linked_dict:
                if linked_dict[key]:
                    ordered_values.append(linked_dict[key])
                recurse_dict(linked_dict[key])

        # #
        max_len = 0
        longest_cycle = None
        for point in all_path_points:
            ordered_values = [point]

            recurse_dict(point)
            if len(ordered_values) > max_len:
                longest_cycle = ordered_values
                max_len = len(ordered_values)

        if not longest_cycle:
            longest_cycle = all_path_points

        # complete cycle
        longest_cycle.append(longest_cycle[0])

        self.all_path_points = longest_cycle
        return self.all_path_points

    def _determine_metrics(self):
        # does it pass

        is_crossing = check_for_self_intersecting(self.all_path_points)
        # boundaries

        x, y = tuple(zip(*self.all_path_points))
        area = poly_area(x, y)

        lenght_of_primary_cycle = len(self.path_locations)

        self.metrics = {}
        self.metrics['is_crossing'] = is_crossing
        self.metrics['area'] = area
        self.metrics['concavity'] = area / lenght_of_primary_cycle

        # distance traveled
        self.metrics['distance'] = total_distance(self.path_locations)
        self.metrics['solidity'] = area / self.metrics['distance']
        self.metrics['all_points'] = self.all_path_points
        self.metrics['grid'] = self.grid_path
        self.metrics['rotations'] = self.grid_rotations

    def run_all(self):
        self._add_kernals()
        self._follow_path()
        self._determine_metrics()

    def return_series(self):
        if self.metrics:
            return pd.Series(self.metrics)
        else:
            return None


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
    # rotations = np.zeros((size, size))
    # rotations[1, 1] = 1
    # rotations[1, 2] = 1
    # #f
    # #
    # rotations = np.zeros((size, size))
    # rotations[1, 1] = 1
    # rotations[1, 2] = 1
    # path = np.array([[1., 2., 0],
    #                  [4., 3., 0],
    #                  [0., 0,0]])

    path = np.array([[1., 6., 5.],
                     [2., 3., 4.],
                     [0., 0., 0.]])

    rotations = np.array([[1, 0, 1],
                          [0, 1, 0],
                          [1, 1, 1]])

    glyph_path = GlyphPath(path, rotations)
    glyph_path.run_all()

    print(glyph_path.metrics)
    save_location = 'glyph_figures/debug_fill_path.png'
    render_path_debug(path, glyph_path.all_path_points, save_location)
