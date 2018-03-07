from generator.node import Node
from bakedrandom import brandom as random
from core.edge import Orientation
from core.floorplan import FloorPlan
from core.room import RoomFactory


class SubdivideTreeToFloorplan(object):

    def __init__(self, lot_width, lot_height, list_o_rooms, rootnode):
        self.lot_width = lot_width
        self.lot_height = lot_height
        self.rootnode = rootnode
        self.list_o_rooms = list_o_rooms

    def generate_candidate_floorplan(self):
        floorplan = FloorPlan([RoomFactory.Rectangle(self.lot_width, self.lot_height)])
        initial_room = floorplan.rooms[0]
        rootscore = self.subdivide_room(floorplan, initial_room, self.rootnode)

        # print(f"Root score is {rootscore}")

        return floorplan

    def subdivide_room(self, floorplan, room, node):
        if len(node.children) <= 1:
            groom = self.list_o_rooms[node.room_indexes[0]]
            room.groom = groom
            node.score = groom.tree_score(room)
            return node.score

        children = node.children[::node.order]

        a1 = sum([ self.list_o_rooms[i].area for i in children[0].room_indexes])
        a2 = sum([ self.list_o_rooms[i].area for i in children[1].room_indexes])

        # a1 = len(node.children[0].room_indexes)
        # a2 = len(node.children[1].room_indexes)

        S = (a1 * (1 - node.t)) / (a1 * (1 - node.t) + a2 * node.t)

        # node.orientation = room.orientation.negate()

        roomA, roomB = floorplan.proportional_subdivide(S, node.orientation, room)
        # TODO: We are not sure what order these things pop out.

        scoreA = self.subdivide_room(floorplan, roomA, children[0])
        scoreB = self.subdivide_room(floorplan, roomB, children[1])
        node.score = min(scoreA, scoreB)
        return node.score


class SubdivideTreeGenerator(object):

    def generate_tree_from_indexes(self, indexes):
        rootnode = Node(
            orientation=random.choice([Orientation.Horizontal, Orientation.Vertical]),
            children=[],
            padding=None,
            order=random.choice([-1, 1]),
            t=0.5,
            room_indexes=list(indexes),
            score=None
        )
        self.generate_tree(rootnode)
        return rootnode

    def generate_tree(self, rootnode):
        if len(rootnode.room_indexes) <= 1:
            return

        # total_area = sum(areas)
        left, right = self.partition_list(rootnode.room_indexes)
        left_child = Node(
            orientation=random.choice([Orientation.Horizontal, Orientation.Vertical]),
            children=[],
            padding=None,
            order=random.choice([-1, 1]),
            t=0.5,
            room_indexes=left,
            score=None
        )
        right_child = Node(
            orientation=random.choice([Orientation.Horizontal, Orientation.Vertical]),
            children=[],
            padding=None,
            order=random.choice([-1, 1]),
            t=0.5,
            room_indexes=right,
            score=None
        )
        rootnode.children.extend([left_child, right_child])
        self.generate_tree(left_child)
        self.generate_tree(right_child)

    def partition_list(self, ls):
        ls = list(ls)
        random.shuffle(ls)
        slice_index = random.randint(1, len(ls) - 1)
        return ls[:slice_index], ls[slice_index:]


