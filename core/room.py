from core.edge import Edge, Orientation

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

    def subdivide(self, x, direction):
        pass # should return two new rooms?

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
        vertex_bottom_right = (x_offset + width + y_offset + height)

        edges = []  # We will hold on to this reference!
        titles = ["Wreck Room"]
        room = Room(edges, titles)

        edge_left = Edge(vertex_bottom_left, vertex_top_left, Direction.Vertical, None, room)
        edge_top = Edge(vertex_top_left, vertex_top_right, Direction.Horizontal, None, room)
        edge_right = Edge(vertex_top_right, vertex_bottom_right, Direction.Vertical, None, room)
        edge_bottom = Edge(vertex_bottom_right, vertex_bottom_left, Direction.Horizontal, None, room)

        # Remember that we're living dangerously and holding onto a reference.
        edges.extend([edge_left, edge_top, edge_right, edge_bottom])
        return room

