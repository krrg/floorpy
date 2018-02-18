from core.edge import Edge, Orientation, EdgeFactory

import numpy as np

class Room(object):

    def __init__(self, edges, label="Room"):
        self.edges = edges
        self.label = label

    @property
    def area(self):
        x = []
        y = []
        for edge in self.edges:
            p = edge.p1_by_sign(self)
            x.append(p[0])
            y.append(p[1])

        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

    @property
    def perimeter(self):
        return sum([edge.length for edge in self.edges])

    def subdivide_edge(self, close_edge):

        if len(close_edge) == 1:
            original_edge = close_edge[0][0]
            subdivide_pt = close_edge[0][1]
            new_edges = original_edge.subdivide(subdivide_pt)

            original_edge_idx = self.edges.index(original_edge)

            new_edges = list(new_edges[::original_edge.sign(self)])

            neighbor_new_edges = new_edges[::-1]
            neighbor = original_edge.opposite_room(self)
            if neighbor is not None:
                neighbor_original_edge_idx = neighbor.edges.index(original_edge)
                neighbor.edges = neighbor.edges[:neighbor_original_edge_idx] + neighbor_new_edges + neighbor.edges[neighbor_original_edge_idx+1:]

            self.edges = self.edges[:original_edge_idx] + new_edges + self.edges[original_edge_idx+1:]


            for e in new_edges:
                e.positive = original_edge.positive
                e.negative = original_edge.negative
        else:
            e0 = close_edge[0][0]
            e1 = close_edge[1][0]

            idx0 = self.edges.index(e0)
            idx1 = self.edges.index(e1)

            # these were originally found in order
            # idx0 whould be lower than idx1
            # they should be neighbors, flip direction if on ends
            assert idx0 < idx1
            if idx0==0 and idx1==len(self.edges)-1:
                new_edges = [e1,e0]
            else:
                new_edges = [e0,e1]

        return new_edges

    def subdivide(self, p, direction):
        assert self.contains(p)

        close_pos_distance = np.inf
        close_pos_edge = []
        close_neg_distance = -np.inf
        close_neg_edge = []
        for e in self.edges:

            interect_pt, dis = e.interect_line(p, direction)
            if dis is None:
                continue
            assert abs(dis) > 1e-8 #make sure we are not setting an edge on the line

            if dis < 0:
                if np.isclose(dis, close_neg_distance):
                    close_neg_edge.append((e, interect_pt))
                elif dis > close_neg_distance:
                    close_neg_edge = [(e, interect_pt)]
                    close_neg_distance = dis

            if dis > 0:
                if np.isclose(dis, close_pos_distance):
                    close_pos_edge.append((e, interect_pt))
                elif dis < close_pos_distance:
                    close_pos_edge = [(e, interect_pt)]
                    close_pos_distance = dis


        pos_0, pos_1 = self.subdivide_edge(close_pos_edge)
        neg_0, neg_1 = self.subdivide_edge(close_neg_edge)


        p0 = pos_0.p1_by_sign(self)
        p1 = neg_0.p1_by_sign(self)

        new_edge = Edge(p0,p1)

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

        room0 = Room(part0)
        room1 = Room(part1)

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
        for e in self.edges:
            v_p = p - e.p0
            v_edge = e.p1 - e.p0

            side = e.sign(self) * np.cross(v_edge, v_p)
            if side <= 0:
                return False
        return True


    @property
    def neighbors(self):
        for n, e in self.neighbors_and_edges:
            yield n

    @property
    def neighbors_and_edges(self):
        for edge in self.edges:
            for room in [edge.positive, edge.negative]:
                if room is not None:
                    yield room, edge

    @property
    def center(self):
        x_max, x_min, y_max, y_min = self.max_min_xy
        return (x_max + x_min) * 0.5, (y_max + y_min) * 0.5

    @property
    def max_min_xy(self):
        x_max, x_min, y_max, y_min = float('-inf'), float('inf'), float('-inf'), float('inf')
        for edge in self.edges:
            for x, y in edge.cartesian_points:
                x_max = max(x_max, x)
                x_min = min(x_min, x)
                y_max = max(y_max, y)
                y_min = min(y_min, y)
        return x_max, x_min, y_max, y_min

# if __name__ == "__main__":

#     p0 = np.array([0,0])
#     p1 = np.array([1,0])
#     p2 = np.array([1,1])
#     p3 = np.array([0,1])

#     edges = [Edge(p0, p1), Edge(p1, p2), Edge(p2,p3), Edge(p3,p0)]
#     room = Room(edges)

#     for e in edges:
#         e.positive = room

#     print(room.contains(np.array([0.5,0.5])))
#     print(room.contains(np.array([1.5,1.5])))

#     room.subdivide(np.array([0.5,0.5]), np.array([1,0]))


class RoomFactory(object):

    @staticmethod
    def Square(width, x_offset=0, y_offset=0):
        return RoomFactory.Rectangle(width, width, x_offset=x_offset, y_offset=y_offset)

    @staticmethod
    def Rectangle(width, height, x_offset=0, y_offset=0):
        p0 = np.array((x_offset, y_offset))
        p1 = np.array((x_offset + width, y_offset))
        p2 = np.array((x_offset + width, y_offset + height))
        p3 = np.array((x_offset, y_offset + height))

        edges = [Edge(p0, p1), Edge(p1, p2), Edge(p2,p3), Edge(p3,p0)]
        room = Room(edges)

        for edge in room.edges:
            edge.positive = room

        return room
