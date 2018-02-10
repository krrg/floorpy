import numpy as np

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

class Edge2(object):

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

        self.negative = None
        self.positive = None

    def subdivide(self, p):
        dist, nearest = pnt2line(p, self.p0, self.p1)
        assert abs(dist) < 1e-4

        e0 = Edge2(self.p0, p)
        e1 = Edge2(p, self.p1)

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

    @property
    def cartesian_points(self):
        return self.p0.tolist(), self.p1.tolist()

    @property
    def center(self):
        return ((self.p0 + self.p1)/2.0).tolist()

if __name__ == "__main__":

    p0 = np.array([  1, 0,   2])
    p1 = np.array([4.5, 0, 0.5])
    p  = np.array([  2, 0, 0.5])

    dist, nearest = pnt2line(p,p0,p1)
    print(dist)
    print(nearest)

    e = Edge2(np.array([0,0]), np.array([2,2]))
    e0, e1 = e.subdivide(np.array([1,1]))

    print(e0.p0)
    print(e0.p1)
    print(e1.p0)
    print(e1.p1)

    ro = np.array([0,0])
    rd = np.array([-1,-1])
    p0 = np.array([1,0])
    p1 = np.array([0,1])
    p = ray_line_intersect(ro,rd,p0,p1)
    print(p)

    # p0 = np.array([0,0])
    # p1 = np.array([1,1])
    # p2 = np.array([1,0])
    # p3 = np.array([0,1])
    # p = seg_intersect(p0,p1,p2,p3)
    # print p
