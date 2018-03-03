import generator.subdivide_tree_generator
from generator.groom import LivingGroom, BedGroom, BathGroom
import itertools


class TreeJudge(object):

    def __init__(self):
        pass

    def create_perfect_floorplan(self):
        max_score = float('-inf')
        best_plan = None

        for i in range(500):

            list_o_rooms = [LivingGroom(4), BedGroom(2), BathGroom(1), BedGroom(2)]
            list_o_rooms = list(itertools.chain(list_o_rooms*4))

            rootnode = generator.subdivide_tree_generator.SubdivideTreeGenerator().generate_tree_from_indexes(range(len(list_o_rooms)))
            g = generator.subdivide_tree_generator.SubdivideTreeToFloorplan(80, 60, list_o_rooms, rootnode)
            fp = g.generate_candidate_floorplan()

            if rootnode.score > max_score:
                best_plan = fp
                max_score = rootnode.score

        print("Max score was", max_score)
        return best_plan


