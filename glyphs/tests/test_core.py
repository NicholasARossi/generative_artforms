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

        self.assertEqual(len(glyph_path.path_locations), np.max(self.path)+1)

class TestKernal(unittest.TestCase):
    def setUp(self) -> None:
        self.centerpoint = [0,0]
        self.radius = 1/3

    def test_hexagon_kernal(self):
        kernal = GlyphKernal(self.centerpoint)
        self.assertGreater(kernal.anchor_radius,kernal.radius)


        self.assertEqual(len(kernal.anchor_points), 6)
        self.assertEqual(len(kernal.shape_points), 6)



if __name__ == '__main__':
    unittest.main()
