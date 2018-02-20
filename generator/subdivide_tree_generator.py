from generator.node import Node
from bakedrandom import brandom as random
from core.edge import Orientation

class SubdivideTreeGenerator(object):

    def generate_tree_from_indexes(self, indexes):
        rootnode = Node(
            orientation=random.choice([Orientation.Horizontal, Orientation.Vertical]),
            children=[],
            padding=None,
            order=random.choice([-1, 1]),
            t=0.5,
            room_indexes=list(indexes),
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
        )
        right_child = Node(
            orientation=random.choice([Orientation.Horizontal, Orientation.Vertical]),
            children=[],
            padding=None,
            order=random.choice([-1, 1]),
            t=0.5,
            room_indexes=right,
        )
        rootnode.children.extend([left_child, right_child])
        self.generate_tree(left_child)
        self.generate_tree(right_child)

    def partition_list(self, ls):
        ls = list(ls)
        random.shuffle(ls)
        slice_index = random.randint(1, len(ls) - 1)
        return ls[:slice_index], ls[slice_index:]


