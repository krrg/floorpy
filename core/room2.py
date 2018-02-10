from edge2 import Edge2
import numpy as np

class Room2(object):

    def __init__(self, edges, label=""):
        self.edges = edges
        self.label = label

    def subdivide_edge(self, close_edge):

        if len(close_edge) == 1:
            original_edge = close_edge[0][0]
            subdivide_pt = close_edge[0][1]
            new_edges = original_edge.subdivide(subdivide_pt)

            original_edge_idx = self.edges.index(original_edge)

            new_edges = list(new_edges[::original_edge.sign(self)])

            self.edges = self.edges[:original_edge_idx] + new_edges + self.edges[original_edge_idx+1:]

            for e in new_edges:
                e.positive = original_edge.positive
                e.negative = original_edge.negative
        else:
            #This isn't quite right
            #need to be sorted by direction
            new_edges = list(close_edge)

        return new_edges

    def subdivide(self, p, direction):
        assert self.contains(p)

        close_pos_distance = np.inf
        close_pos_edge = []
        close_neg_distance = -np.inf
        close_neg_edge = []
        print "Start Subdivide Search..."
        print len(self.edges)
        for e in self.edges:

            interect_pt, dis = e.interect_line(p, direction)
            print e, dis
            if dis is None:
                continue
            assert abs(dis) > 1e-8 #make sure we are not setting an edge on the line

            if dis < 0:
                if dis == close_neg_distance:
                    close_neg_edge.append((e, interect_pt))
                elif dis > close_neg_distance:
                    close_neg_edge = [(e, interect_pt)]

            if dis > 0:
                if dis == close_pos_distance:
                    close_pos_edge.append((e, interect_pt))
                elif dis < close_pos_distance:
                    close_pos_edge = [(e, interect_pt)]


        pos_0, pos_1 = self.subdivide_edge(close_pos_edge)
        neg_0, neg_1 = self.subdivide_edge(close_neg_edge)


        p0 = pos_0.p1_by_sign(self)
        p1 = neg_0.p1_by_sign(self)

        new_edge = Edge2(p0,p1)

        pos_idx_0 = self.edges.index(pos_0)
        pos_idx_1 = self.edges.index(pos_1)

        neg_idx_0 = self.edges.index(neg_0)
        neg_idx_1 = self.edges.index(neg_1)

        if pos_idx_1 < neg_idx_0:
            part0 = [new_edge] + self.edges[pos_idx_1:neg_idx_0+1]
        else:
            part0 = self.edges[:neg_idx_0+1] + [new_edge] + self.edges[pos_idx_1:]

        if neg_idx_1 < pos_idx_0:
            part1 = self.edges[neg_idx_1:pos_idx_0+1] + [new_edge]
        else:
            part1 = self.edges[:pos_idx_0+1] + [new_edge] + self.edges[neg_idx_1:]

        room0 = Room2(part0)
        room1 = Room2(part1)

        # print "Subdivide Side"
        # print pos_1.p0
        # print pos_1.p1
        # print pos_1.sign(self)
        # print p1
        # print p0
        # print "^^^^^^^^^^^^^^"

        # We use pos_1 because the edges will always be inserted
        # after it. We could have used any of the split edges
        v = pos_1.p1 - pos_1.p0
        if pos_1.sign(self) * np.cross(p1-p0, v) > 0:
            new_edge.positive = room0
            new_edge.negative = room1
        else:
            new_edge.positive = room1
            new_edge.negative = room0

        for e in part0:
            e.replace_room(self, room0)

        for e in part1:
            e.replace_room(self, room1)


        return room0, room1

    def contains(self, p):
        print ""
        print "Searching for ", p
        for e in self.edges:
            print e.p0, e.p1
        print "-----"

        for e in self.edges:
            v_p = p - e.p0
            v_edge = e.p1 - e.p0

            print e.p0, e.p1, v_p, e.sign(self), np.cross(v_edge, v_p)
            side = e.sign(self) * np.cross(v_edge, v_p)
            if side <= 0:
                print "Failed Search"
                return False
        print "Success Search"
        return True


    @property
    def neighbors(self):
        for edge in self.edges:
            for room in [edge.positive, edge.negative]:
                if room is not None:
                    yield room

    @property
    def center(self):
        x_max, x_min, y_max, y_min = float('-inf'), float('inf'), float('-inf'), float('inf')
        for edge in self.edges:
            for x, y in edge.cartesian_points:
                x_max = max(x_max, x)
                x_min = min(x_min, x)
                y_max = max(y_max, y)
                y_min = min(y_min, y)

        return (x_max + x_min) * 0.5, (y_max + y_min) * 0.5

if __name__ == "__main__":

    p0 = np.array([0,0])
    p1 = np.array([1,0])
    p2 = np.array([1,1])
    p3 = np.array([0,1])

    edges = [Edge2(p0, p1), Edge2(p1, p2), Edge2(p2,p3), Edge2(p3,p0)]
    room = Room2(edges)

    for e in edges:
        e.positive = room

    print room.contains(np.array([0.5,0.5]))
    print room.contains(np.array([1.5,1.5]))

    room.subdivide(np.array([0.5,0.5]), np.array([1,0]))
