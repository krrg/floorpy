from core.edge import Edge, Orientation, EdgeFactory

class Room(object):

    def __init__(self, edges, label="Room"):
        self.edges = edges
        self.label = label

    def area(self):
        return 0

    @property
    def center(self):
        x_max, x_min, y_max, y_min = float('-inf'), float('inf'), float('-inf'), float('inf')
        for edge in self.edges:
            for x, y in edge.cartesian_points:
                x_max = max(x_max, x)
                x_min = min(x_min, x)
                y_max = max(y_max, y)
                y_min = min(y_min, y)
                print(x, y)

        print("this is room ", self)

        return (x_max + x_min) * 0.5, (y_max + y_min) * 0.5

    def find_nearest_edge_in_direction(self, orientation, sign, x, y):
        if orientation == Orientation.Horizontal:
            z_start, v = y, x
        elif orientation == Orientation.Vertical:
            z_start, v = x, y

        oriented_edges = filter(lambda edge: edge.orientation == orientation, self.edges)
        ray_hit_edges = filter(lambda edge: edge.contains(v), oriented_edges)
        correct_sign_edges = filter(lambda edge: (edge.z - z_start) * sign > 0, ray_hit_edges)  # This is either > or <
        correct_sign_edges = list(correct_sign_edges)

        if not correct_sign_edges:
            return []

        closest_edge = min(correct_sign_edges, key=lambda edge: abs(edge.z - z_start))
        closest_edge_dist = abs(closest_edge.z - z_start)
        # If we hit the corner, then may be multiple closest edges
        matching_edges = filter(lambda edge: abs(edge.z - z_start) == closest_edge_dist, correct_sign_edges)
        return list(matching_edges)

    def find_nearest_edge_in_positive(self, orientation, x, y):
        return self.find_nearest_edge_in_direction(orientation, 1, x, y)

    def find_nearest_edge_in_negative(self, orientation, x, y):
        return self.find_nearest_edge_in_direction(orientation, -1, x, y)

    def point_on_edge(self, x, y):
        return any([edge.strict_contains(x, y) for edge in self.edges])

    def contains(self, x, y, neg_edge_hint=None, pos_edge_hint=None, orientation_hint=Orientation.Horizontal):
        if self.point_on_edge(x, y):
            return False

        if not neg_edge_hint:
            neg_edge_hint = self.find_nearest_edge_in_negative(orientation_hint, x, y)
        if not pos_edge_hint:
            pos_edge_hint = self.find_nearest_edge_in_positive(orientation_hint, x, y)

        if len(neg_edge_hint) == 0 or len(pos_edge_hint) == 0:
            return False

        neg_edge_hint, pos_edge_hint = neg_edge_hint[0], pos_edge_hint[0]

        # Kind of lazy, assume no weirdly shaped rooms
        neg_rooms = set([
            neg_edge_hint.left,
            neg_edge_hint.right
        ])

        pos_rooms = set([
            pos_edge_hint.left,
            pos_edge_hint.right,
        ])

        return self in (neg_rooms & pos_rooms)

    def subdivide_edges(self, x, y, edges):
        if len(edges) == 1:
            edge = edges[0]
            return edge.subdivide(edge.project_to_v(x, y))
        else:
            edge0, edge1 = edges
            return edge0, edge1


    def subdivide(self, x, y, orientation_of_new_wall):
        neg_edge = self.find_nearest_edge_in_negative(orientation_of_new_wall.negate(), x, y)
        pos_edge = self.find_nearest_edge_in_positive(orientation_of_new_wall.negate(), x, y)

        if not self.contains(x, y, neg_edge_hint=neg_edge, pos_edge_hint=pos_edge):
            raise SubdivisionOutOfBoundsException()

        edge0, edge1 = self.subdivide_edges(x, y, neg_edge)
        edge2, edge3 = self.subdivide_edges(x, y, pos_edge)

        # Figure out which indexes to draw the edge across at.
        split_index_1 = max(self.edges.index(edge0), self.edges.index(edge1))
        split_index_2 = max(self.edges.index(edge2), self.edges.index(edge3))

        if split_index_1 > split_index_2:
            split_index_1, split_index_2 = split_index_2, split_index_1

        roomA = Room([])
        roomB = Room([])

        new_edge = Edge(neg_edge[0].z, pos_edge[0].z, neg_edge[0].project_to_v(x, y), orientation_of_new_wall, roomB, roomA)

        # Sketchy, don't do this at home.
        roomA.edges = self.edges[:split_index_1] + [new_edge] + self.edges[split_index_2:]
        roomB.edges = [new_edge] + self.edges[split_index_1:split_index_2]

        for edge in roomA.edges:
            edge.replace_room(self, roomA)

        for edge in roomB.edges:
            edge.replace_room(self, roomB)

        return roomB, roomA


    def replace_edge(self, old_edge, edgeA, edgeB):
        old_index = self.edges.index(old_edge)
        self.edges.insert(old_index, edgeB)
        self.edges.insert(old_index, edgeA)
        self.edges.remove(old_edge)

    @property
    def neighbors(self):
        for edge in self.edges:
            for room in [edge.adj_room_left, edge.adj_room_right]:
                if room is not None:
                    yield room


class SubdivisionOutOfBoundsException(Exception):
    pass


class RoomFactory(object):

    @staticmethod
    def Square(width, x_offset=0, y_offset=0):
        return RoomFactory.Rectangle(width, width, x_offset=x_offset, y_offset=y_offset)

    @staticmethod
    def Rectangle(width, height, x_offset=0, y_offset=0):
        vertex_top_left = (x_offset, y_offset)
        vertex_top_right = (x_offset + width, y_offset)
        vertex_bottom_left = (x_offset, y_offset + height)
        vertex_bottom_right = (x_offset + width, y_offset + height)

        edges = []  # We will hold on to this reference!
        room = Room(edges)

        edge_left = EdgeFactory.create_edge_from_points(vertex_bottom_left, vertex_top_left, room_right=room)
        edge_top = EdgeFactory.create_edge_from_points(vertex_top_left, vertex_top_right,  room_right=room)
        edge_right = EdgeFactory.create_edge_from_points(vertex_top_right, vertex_bottom_right, room_right=room)
        edge_bottom = EdgeFactory.create_edge_from_points(vertex_bottom_right, vertex_bottom_left, room_right=room)

        # Remember that we're living dangerously and holding onto a reference.
        edges.extend([edge_left, edge_top, edge_right, edge_bottom])
        return room
