import math
import numpy as np

from glyphs.utilities import hexagon_vertices,\
    compare_points, generate_slope, close_compare





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

        for i, kernal in enumerate(self.kernals[:-1]):
            all_path_points.append(current_point)

            target_slope = generate_slope(self.kernals[i].center_point,
                                          self.kernals[i + 1].center_point)



            self.kernals[i].recurse_shape_points(current_point,
                                                 target_slope)
            all_path_points.extend(self.kernals[i].subpath)

            # leap to next kernal
            if self.kernals[i].rotation == self.kernals[i + 1].rotation:
                # we find the point on the next kernal that has the target slope
                current_point = self.kernals[i + 1].find_point_on_slope(all_path_points[-1], target_slope)
            else:
                pass

        return all_path_points


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

        anchor_points_extended = self.anchor_points
        anchor_points_extended.append(self.anchor_points[0])
        self.anchor_points_with_rotation = {}

        if self.rotation == 'ccw':
            anchor_points = self.anchor_points[::-1]
        else:
            anchor_points = self.anchor_points

        for i,s in enumerate(self.shape_points):

            self.anchor_points_with_rotation[s] = anchor_points[i-1]

    def recurse_shape_points(self,
                             point,
                             target_slope):
        next_shape_point = self.shape_points_with_rotation[point]
        next_anchor_point = self.anchor_points_with_rotation[point]
        current_shape_slope = generate_slope(point, next_shape_point)
        current_anchor_slope = generate_slope(point, next_anchor_point)
        # make a note (1.6666666666666667, 0.5773502691896257) --> (2.0, 0.5773502691896258)


        if close_compare(current_anchor_slope, target_slope):
            self.subpath.append(next_anchor_point)
            return self.subpath
        # elif close_compare(current_shape_slope, target_slope):
        #     self.subpath.append(next_shape_point)
        #
        #     return self.subpath


        else:
            self.subpath.append(next_shape_point)
            self.recurse_shape_points(next_shape_point, target_slope)

    def find_point_on_slope(self,
                            current_point,
                            slope):
        matches = {}
        for point in self.shape_points:
            if close_compare(generate_slope(current_point, point), slope):
                matches[math.dist(current_point, point)] = point

        try:
            return matches[min(matches.keys())]
        except:
            print('bug')

if __name__ == '__main__':
    from glyphs.visualization import render_path_debug

    """
    Structure of algorithm
    pick random point on first kernal
    cycle in intendended direction
    
    when slope of last lines equeals slope between then we leap
    
    leep to next kernal
    
    
    """
    size = 3
    path = np.zeros((size, size))
    path[0, 0] = 1
    path[1, 0] = 2
    path[1, 1] = 3
    path[2, 1] = 4
    path[2, 2] = 5
    path[1, 2] = 6
    path[0, 2] = 7
    path[0, 1] = 8

    path[0, 0] = 1
    path[0, 1] = 2
    # path[1, 1] = 3
    # path[1, 2] = 4


    glyph_path = GlyphPath(path)
    glyph_path.add_kernals()
    all_points = glyph_path.follow_path()
    save_location = 'glyph_figures/fine_path.png'
    render_path_debug(path, all_points, save_location)
