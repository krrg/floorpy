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

        edge0 = Edge(self.v0, v, self.z, self.orientation, self.adj_room_left, self.adj_room_right)
        edge1 = Edge(v, self.v1, self.z, self.orientation, self.adj_room_left, self.adj_room_right)

        if self.adj_room_left:
            self.adj_room_left.replace_edge(self, edge1, edge0)
        if self.adj_room_right:
            self.adj_room_right.replace_edge(self, edge0, edge1)

        return edge0, edge1

    def contains(self, v):
        min_v = min(self.v0, self.v1)
        max_v = max(self.v0, self.v1)
        result = min_v <= v <= max_v
        print(f"My name is edge {self.v0} to {self.v1}, and I feel that {v} {result} in my coordinates.")
        return result

    def strict_contains(self, x, y):
        if self.orientation == Orientation.Horizontal:
            v, z = x, y
        else:
            v, z = y, x
        return self.contains(v) and self.z == z

    def project_to_v(self, x, y):
        return x if self.orientation == Orientation.Horizontal else y

    @property
    def cartesian_points(self):
        if self.orientation == Orientation.Horizontal:
            return ((self.v0, self.z), (self.v1, self.z))
        else:
            return ((self.z, self.v0), (self.z, self.v1))

    def replace_room(self, old_room, new_room):
        if self.adj_room_left is old_room:
            self.adj_room_left = new_room
        if self.adj_room_right is old_room:
            self.adj_room_right = new_room

    @property
    def left(self):
        return self.adj_room_left

    @property
    def right(self):
        return self.adj_room_right

    def __str__(self):
        return str(self.cartesian_points)

    def __repr__(self):
        return self.__str__()


class EdgeFactory(object):

    @staticmethod
    def create_edge(x0, y0, x1, y1, room_left=None, room_right=None):
        if x0 == x1:
            return Edge(y0, y1, x0, Orientation.Vertical, room_left, room_right)
        elif y0 == y1:
            return Edge(x0, x1, y0, Orientation.Horizontal, room_left, room_right)
        else:
            raise InvalidEdgeSubdivision()

    @staticmethod
    def create_edge_from_points(p0, p1, room_left=None, room_right=None):
        x0, y0 = p0
        x1, y1 = p1
        return EdgeFactory.create_edge(x0, y0, x1, y1, room_left=room_left, room_right=room_right)


class InvalidEdgeSubdivision(Exception):
    pass

import enum

class Orientation(enum.Enum):
    Horizontal = "Horizontal"
    Vertical = "Vertical"

    def negate(self):
        return Orientation.Horizontal if self == Orientation.Vertical else Orientation.Vertical


