import unittest
from core.room import Room, RoomFactory
from core.edge import Edge, EdgeFactory, Orientation

class EdgeTestCases(unittest.TestCase):

    def test_edge_subdivide(self):
        room = RoomFactory.Rectangle(10, 12)
        # edge_left = room.edges[0]
        # edge_right = room.edges[2]
        # edge_right.subdivide(4)
        # self.assertTrue(len(room.edges) == 5)
        # edge_left.subdivide(4)
        # self.assertTrue(len(room.edges) == 6)

        # roomA, roomB = room.subdivide(4, 4, Orientation.Horizontal)
        # print("A", "\n".join(map(str, roomA.edges)))
        # print()
        # print("B", "\n".join(map(str, roomB.edges)))

        roomA, roomB = room.subdivide(4, 4, Orientation.Horizontal)
        print("A", "\n".join(map(str, roomA.edges)))
        print()
        print("B", "\n".join(map(str, roomB.edges)))

        print("RoomA contains 2, 6?", roomA.contains(6, 2))

        # Todo, assert the ordering of coordinates is that
        # ((0, 12), (0, 4))
        # ((0, 4), (0, 0))
        # ((0, 0), (10, 0))
        # ((10, 0), (10, 4))
        # ((10, 4), (10, 12))
        # ((10, 12), (0, 12))
