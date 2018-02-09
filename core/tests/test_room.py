import unittest
from core.edge import Edge, EdgeFactory, Orientation
from core.room import Room, RoomFactory

class RoomTestCase(unittest.TestCase):

    def test_find_nearest_edge_0(self):
        room = Room([EdgeFactory.create_edge(0, 0, 0, 5)])

        edgesA = room.find_nearest_edge_in_positive(Orientation.Vertical, -5, 3)
        edgesB = room.find_nearest_edge_in_negative(Orientation.Vertical, -5, 3)
        edgesC = room.find_nearest_edge_in_positive(Orientation.Horizontal, -5, 3)
        edgesD = room.find_nearest_edge_in_negative(Orientation.Horizontal, -5, 3)

        self.assertEqual(1, len(edgesA))
        self.assertEqual(0, len(edgesB))
        self.assertEqual(0, len(edgesC))
        self.assertEqual(0, len(edgesD))

    def test_find_nearest_edge_1(self):
        room = Room([EdgeFactory.create_edge(0, 0, 5, 0)])

        edgesA = room.find_nearest_edge_in_positive(Orientation.Vertical, 3, 5)
        edgesB = room.find_nearest_edge_in_negative(Orientation.Vertical, 3, 5)
        edgesC = room.find_nearest_edge_in_positive(Orientation.Horizontal, 3, 5)
        edgesD = room.find_nearest_edge_in_negative(Orientation.Horizontal, 3, 5)

        self.assertEqual(0, len(edgesA))
        self.assertEqual(0, len(edgesB))
        self.assertEqual(0, len(edgesC))
        self.assertEqual(1, len(edgesD))

    def test_find_nearest_edge_2(self):
        edges = [
            EdgeFactory.create_edge(0, 0, 0, 5),
            EdgeFactory.create_edge(0, 5, 0, 10)
        ]
        room = Room(edges)

        edgesA = room.find_nearest_edge_in_positive(Orientation.Vertical, 5, 5)
        edgesB = room.find_nearest_edge_in_negative(Orientation.Vertical, 5, 5)
        edgesC = room.find_nearest_edge_in_positive(Orientation.Horizontal, 5, 5)
        edgesD = room.find_nearest_edge_in_negative(Orientation.Horizontal, 5, 5)

        self.assertEqual(0, len(edgesA))
        self.assertEqual(2, len(edgesB))
        self.assertEqual(0, len(edgesC))
        self.assertEqual(0, len(edgesD))

    def test_contains_rectangle_0(self):
        room = RoomFactory.Rectangle(10, 10)

        self.assertTrue(room.contains(5, 5))
        self.assertFalse(room.contains(100, 100))
        self.assertFalse(room.contains(5, 15))
        self.assertFalse(room.contains(15, 5))
        self.assertFalse(room.contains(-10, 5))
        self.assertFalse(room.contains(5, -10))

    def test_contains_rectangle_0(self):
        room = RoomFactory.Rectangle(12, 10)

        self.assertFalse(room.contains(0, 0))
        self.assertFalse(room.contains(0, 10))
        self.assertFalse(room.contains(12, 0))
        self.assertFalse(room.contains(12, 10))

        self.assertTrue(room.point_on_edge(0, 5))
        self.assertTrue(room.point_on_edge(6, 10))
        self.assertTrue(room.point_on_edge(6, 0))
        self.assertTrue(room.point_on_edge(12, 5))

    def test_center_point(self):
        room = RoomFactory.Rectangle(14, 16)
        self.assertTrue(room.center == (7.0, 8.0))
