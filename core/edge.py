class Edge(object):

    def __init__(self, v0, v1, z, horz_or_vert, adj_room_left_01, adj_room_left_10):
        self.v0 = v0
        self.v1 = v1
        self.z = z
        self.orientation = horz_or_vert
        self.adj_room_left = adj_room_left_01
        self.adj_room_right = adj_room_left_10

    def subdivide(self, v):
        if not self.contains(v):
            raise InvalidEdgeSubdivision("Subdivision point is not between vertices.")

        edge0 = Edge(v0, v, self.orientation, self.adj_room_left, self.adj_room_right)
        edge1 = Edge(v, v1, self.orientation, self.adj_room_left, self.adj_room_right)

        self.adj_room_left.replace_edge(self, edge1, edge0)
        self.adj_room_right.replace_edge(self, edge0, edge1)

        return edge0, edge1

    def contains(self, v):
        min_v = min(self.v0, self.v1)
        max_v = max(self.v0, self.v1)
        return min_v <= v <= max_v


class EdgeFactory(object):

    @staticmethod
    def create_edge(x0, y0, x1, y1):
        if x0 == x1:
            return Edge(y0, y1, x0, Orientation.Vertical, None, None)
        elif y0 == y1:
            return Edge(x0, x1, y0, Orientation.Horizontal, None, None)
        else:
            raise InvalidEdgeSubdivision()


class InvalidEdgeSubdivision(Exception):
    pass

import enum

class Orientation(enum.Enum):
    Horizontal = "Horizontal"
    Vertical = "Vertical"

