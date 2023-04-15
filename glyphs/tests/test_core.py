import unittest
from glyphs.core import GlyphPath, GlyphKernal
import numpy as np


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

    def test_glyph_path(self):
        glyph_path = GlyphPath(self.path)

        self.assertEqual(len(glyph_path.path_locations), np.max(self.path) + 1)

    def test_add_kernals(self):
        glyph_path = GlyphPath(self.path)
        glyph_path.add_kernals()
        self.assertEqual(len(glyph_path.kernals), np.max(self.path) + 1)

    def test_follow_path(self):
        glyph_path = GlyphPath(self.path)
        glyph_path.add_kernals()
        glyph_path.follow_path()

class TestKernal(unittest.TestCase):
    def setUp(self) -> None:
        self.centerpoint = [0, 0]
        self.radius = 1 / 3

    def test_hexagon_kernal(self):
        kernal = GlyphKernal(self.centerpoint)
        self.assertGreater(kernal.anchor_radius, kernal.radius)

        self.assertEqual(len(kernal.anchor_points), 7)


class IntegrationTest(unittest.TestCase):
    def test_large_circle(self):
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
        glyph_path = GlyphPath(path)
        glyph_path.add_kernals()
        all_points = glyph_path.follow_path()
        self.assertEqual(len(all_points),29)

    def test_small_circle(self):
        size = 3
        path = np.zeros((size, size))
        path[0, 0] = 1
        path[0, 1] = 2
        glyph_path = GlyphPath(path)
        glyph_path.add_kernals()
        all_points = glyph_path.follow_path()
        self.assertEqual(len(all_points) , 10)

if __name__ == '__main__':
    unittest.main()
