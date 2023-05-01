import unittest
from glyphs.core import GlyphPath, GlyphKernal
import numpy as np
from glyphs.utilities import poly_area

class TestPath(unittest.TestCase):
    def setUp(self) -> None:
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
        self.path = path
        self.rotations = np.zeros((size, size))

    def test_glyph_path(self):
        glyph_path = GlyphPath(self.path,self.rotations)

        self.assertEqual(len(glyph_path.path_locations), np.max(self.path) + 1)

    def test_add_kernals(self):
        glyph_path = GlyphPath(self.path,self.rotations)
        glyph_path._add_kernals()
        self.assertEqual(len(glyph_path.kernals), np.max(self.path) )

    def test_follow_path(self):
        glyph_path = GlyphPath(self.path,self.rotations)
        glyph_path.run_all()

class TestKernal(unittest.TestCase):
    def setUp(self) -> None:
        self.centerpoint = [0, 0]
        self.radius = 1 / 3

    def test_hexagon_kernal(self):
        kernal = GlyphKernal(self.centerpoint)
        self.assertGreater(kernal.anchor_radius, kernal.radius)

        self.assertEqual(len(kernal.anchor_points), 6)


class IntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
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
        self.large_path = path

        rotations = np.zeros((size, size))
        rotations[1, 1] = 1
        rotations[1, 2] = 1
        self.large_rotation = rotations
        self.zero_rotations = np.zeros((size, size))

    def test_large_circle(self):

        glyph_path = GlyphPath(self.large_path,self.zero_rotations)
        glyph_path.run_all()
        self.assertEqual(len(glyph_path.all_path_points),31)

    def test_small_circle(self):
        size = 3
        path = np.zeros((size, size))
        path[0, 0] = 1
        path[0, 1] = 2
        glyph_path = GlyphPath(path,np.zeros((size, size)))
        glyph_path.run_all()
        self.assertEqual(len(glyph_path.all_path_points) , 13)

    def test_area(self):
        glyph_path = GlyphPath(self.large_path, self.large_rotation)
        glyph_path.run_all()
        xs =[]
        ys = []
        for x,y in glyph_path.all_path_points:
            xs.append(x)
            ys.append(y)
        self.assertAlmostEqual(poly_area(xs,ys),4.0414855649999915)



if __name__ == '__main__':
    unittest.main()
