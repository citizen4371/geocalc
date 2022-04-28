import unittest
from geocalc.geometry import Rectangle

class GeometryTestCase(unittest.TestCase):
    def make_rec(self, tpl):
        return Rectangle.from_tuple(tpl)

    def test_rectangle_creation(self):
        self.make_rec((0, 10, 10, 0))

        with self.assertRaisesRegex(ValueError, 'should be to the right of top left'):
            self.make_rec((0, 0, 0, 0))

        with self.assertRaisesRegex(ValueError, 'should be lower than top left'):
            self.make_rec((0, 0, 1, 1))

        with self.assertRaisesRegex(ValueError, 'should be lower than top left'):
            self.make_rec((0, 1, 1, 2))

        with self.assertRaisesRegex(ValueError, 'should be to the right of top left'):
            self.make_rec((1, 1, 0, 0))


    def test_rectangle_intersection(self):
        for b1, b2, expected in (
            ((0, 10, 10, 0), (0, 10, 10, 0), (0, 10, 10, 0)),
            ((0, 10, 10, 0), (0, 5, 5, 0), (0, 5, 5, 0)),
            ((6, 10, 10, 6), (0, 6.1, 6.1, 0), (6, 6.1, 6.1, 6)),
            ((5, 10, 10, 6), (6.5, 7.1, 9.5, 4), (6.5, 7.1, 9.5, 6)),
            ((5, 10, 10, 6), (9, 100, 9.5, 0), (9, 10, 9.5, 6)),
            ((6, 10, 10, 6), (0, 5, 5, 0), None),
            ((0, 10, 5, 5), (3, 3, 10, 0), None),
            ((0.1, 10.1, 10.1, 5.1), (0, 5.1, 10.1, 0), None),
        ):
            box1 = self.make_rec(b1)
            box2 = self.make_rec(b2)

            expected_rec = (expected and self.make_rec(expected))

            self.assertEqual(
                box1.intersection(box2), 
                expected_rec, 
                msg=f'Intersection of {box2} and {box1} is expected to be {expected_rec}')
            
            self.assertEqual(
                box2.intersection(box1), 
                expected_rec, 
                msg=f'Intersection of {box2} and {box1} is not commutative')

    def test_rectangle_iou(self):
        for b1, b2, expected_iou in (
            ((0, 10, 10, 0), (0, 10, 10, 0), 1),
            ((0, 10, 10, 0), (5, 10, 10, 0), 0.5),
            ((0, 10, 10, 0), (5, 10, 15, 0), 0.333),
            ((0, 10, 10, 0), (2.4, 4.3, 7.4, 2.3), 0.1),
            ((2, 3, 4, 1), (3, 2, 5, 0), 0.143),
            ((5, 10, 10, 5), (0, 5, 5, 0), 0),
        ):
            box1 = self.make_rec(b1)
            box2 = self.make_rec(b2)

            self.assertAlmostEqual(
                box1.iou(box2), expected_iou, places=3,
                msg=f'IoU of {box1} and {box2} should be {expected_iou}')
