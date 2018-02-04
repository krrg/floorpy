from core.edge import Edge, Orientation, EdgeFactory

class Room(object):

    def __init__(self, edges, titles):
        self.edges = edges
        self.titles = titles

    def area(self):
        return 0

    def is_complete(self):
        return len(self.titles) == 1

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



    def subdivide(self, x, y, orientation_of_new_wall):
        neg_edge = self.find_nearest_edge_in_negative(orientation_of_new_wall.negate(), x, y)
        pos_edge = self.find_nearest_edge_in_positive(orientation_of_new_wall.negate(), x, y)


    def replace_edge(self, old_edge, edgeA, edgeB):
        old_index = self.edges.index(old_edge)
        self.edges.insert(old_index, edgeB)
        self.edges.insert(old_index, edgeA)


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
        titles = ["Wreck Room"]
        room = Room(edges, titles)

        edge_left = EdgeFactory.create_edge_from_points(vertex_bottom_left, vertex_top_left, room_right=room)
        edge_top = EdgeFactory.create_edge_from_points(vertex_top_left, vertex_top_right,  room_right=room)
        edge_right = EdgeFactory.create_edge_from_points(vertex_top_right, vertex_bottom_right, room_right=room)
        edge_bottom = EdgeFactory.create_edge_from_points(vertex_bottom_right, vertex_bottom_left, room_right=room)

        # Remember that we're living dangerously and holding onto a reference.
        edges.extend([edge_left, edge_top, edge_right, edge_bottom])
        return room

