import numpy as np
from core.opening import Window, Door


class Edge(object):

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

        self.negative = None
        self.positive = None

        self.doors = []
        self.windows = []

    @property
    def is_outside_edge(self):
        return self.negative is None or self.positive is None

    def subdivide(self, p):
        dist, nearest = pnt2line(p, self.p0, self.p1)
        assert abs(dist) < 1e-4

        e0 = Edge(self.p0, p)
        e1 = Edge(p, self.p1)

        e0.positive = self.positive
        e1.positive = self.positive

        e0.negative = self.negative
        e1.negative = self.negative

        return e0, e1

    def sign(self, room):
        if room is self.positive:
            return 1
        if room is self.negative:
            return -1
        raise Exception("No sign for requested room")

    def p1_by_sign(self, room):
        if self.sign(room) == 1:
            return self.p1
        return self.p0

    def replace_room(self, old_room, new_room):
        if self.positive is old_room:
            self.positive = new_room
        if self.negative is old_room:
            self.negative = new_room

    def opposite_room(self, room):
        if self.positive is room:
            return self.negative
        if self.negative is room:
            return self.positive
        raise Exception("Invalid opposite room request")

    def interect_line(self, ro, rd):
        return ray_line_intersect(ro, rd, self.p0, self.p1)

    def insert_opening(self, opening):
        if isinstance(opening, Door):
            self.doors.append(opening)
        elif isinstance(opening, Window):
            self.windows.append(opening)
        else:
            raise Exception("Not an opening I can deal with.")

    def interpolate_at(self, t):
        return (1 - t) * self.p0 + t * self.p1

    @property
    def unit_vector(self):
        direction_vector = self.p1 - self.p0
        direction_vector = direction_vector / np.linalg.norm(direction_vector)
        return direction_vector

    def radial_points(self, t, radius):
        center = self.interpolate_at(t)
        unit = self.unit_vector
        a = center + radius * unit
        b = center - radius * unit
        return a, b

    @property
    def cartesian_points(self):
        return self.p0.tolist(), self.p1.tolist()

    @property
    def center(self):
        return ((self.p0 + self.p1)/2.0).tolist()

    def contains(self, point):
        a, b = self.cartesian_points
        return is_on(a, b, point)


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


# if __name__ == "__main__":

#     p0 = np.array([  1, 0,   2])
#     p1 = np.array([4.5, 0, 0.5])
#     p  = np.array([  2, 0, 0.5])

#     dist, nearest = pnt2line(p,p0,p1)
#     print(dist)
#     print(nearest)

#     e = Edge(np.array([0,0]), np.array([2,2]))
#     e0, e1 = e.subdivide(np.array([1,1]))

#     print(e0.p0)
#     print(e0.p1)
#     print(e1.p0)
#     print(e1.p1)

#     ro = np.array([0,0])
#     rd = np.array([-1,-1])
#     p0 = np.array([1,0])
#     p1 = np.array([0,1])
#     p = ray_line_intersect(ro,rd,p0,p1)
#     print(p)

    # p0 = np.array([0,0])
    # p1 = np.array([1,1])
    # p2 = np.array([1,0])
    # p3 = np.array([0,1])
    # p = seg_intersect(p0,p1,p2,p3)
    # print p

def pnt2line(pnt, start, end):

    pnt = pnt.astype(np.float32)
    start = start.astype(np.float32)
    end = end.astype(np.float32)

    #based on http://www.fundza.com/vectors/point2line/index.html
    line_vec = end - start
    pnt_vec = pnt - start

    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    pnt_vec_scaled = pnt_vec / line_len

    t = np.dot(line_unitvec, pnt_vec_scaled)

    nearest = None
    dist = None
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    else:
        nearest = line_vec * t
        dist = np.linalg.norm(nearest - pnt_vec)
        nearest = start + nearest
    return dist, nearest


# https://gist.github.com/danieljfarrell/faf7c4cafd683db13cbc
def ray_line_intersect(rayOrigin, rayDirection, point1, point2):

    rayOrigin = rayOrigin.astype(np.float32)
    rayDirection = rayDirection.astype(np.float32)
    point1 = point1.astype(np.float32)
    point2 = point2.astype(np.float32)

    rayDirection = rayDirection / np.linalg.norm(rayDirection)
    v1 = rayOrigin - point1
    v2 = point2 - point1
    v3 = np.array([-rayDirection[1], rayDirection[0]])


    d = np.dot(v2, v3)

    if d == 0:
        return None, None

    t1 = np.cross(v2, v1) / d
    t2 = np.dot(v1, v3) / d

    if t2 >= 0.0 and t2 <= 1.0:
        return rayOrigin + t1 * rayDirection, t1
    return None, None


# Shamelessly taken from https://stackoverflow.com/questions/328107
def is_on(a, b, c):
    "Return true iff point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    return (collinear(a, b, c)
            and (within(a[0], c[0], b[0]) if a[0] != b[0] else
                 within(a[1], c[1], b[1])))

def collinear(a, b, c):
    "Return true iff a, b, and c all lie on the same line."
    return (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])

def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p
