class Edge(object):

    def __init__(self, v0, v1, horz_or_vert, adj_room_left_01, adj_room_left_10):
        self.v0 = v0
        self.v1 = v1
        self.direction = horz_or_vert
        self.adj_room_left = adj_room_left_01
        self.adj_room_right = adj_room_left_10

    def subdivide(self, v):
        if not v0 < v < v1:
            raise InvalidEdgeSubdivision("Subdivision point is not between vertices.")

        edge0 = Edge(v0, v, self.direction, self.adj_room_left, self.adj_room_right)
        edge1 = Edge(v, v1, self.direction, self.adj_room_left, self.adj_room_right)

        return edge0, edge1



class InvalidEdgeSubdivision(Exception):
    pass

import enum
class Direction(enum.Enum):
    Horizontal = enum.auto()
    Vertical = enum.auto()


class InvalidDirectionError(Exception):
    pass
