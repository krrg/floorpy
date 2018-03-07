import generator.subdivide_tree_generator
from generator.groom import LivingGroom, BedGroom, BathGroom
import itertools
from generator.genetic_tree_shaker import GeneticTreeShaker
from generator.subdivide_tree_generator import *
from generator.groom import *
import renderer.svgrenderer


class TreeJudge(object):

    def __init__(self):
        pass

    def create_perfect_floorplan(self):
        max_score = float('-inf')
        best_plan = None

        for i in range(5):
            print("We are evaluating population ", i)

            list_o_rooms = [LivingGroom(4), BedGroom(2), BathGroom(1), BedGroom(2)] + [LivingGroom(4), BedGroom(2), BathGroom(1), BedGroom(2)]
    # list_o_rooms = list(itertools.chain(list_o_rooms*3))

            adam = SubdivideTreeGenerator().generate_tree_from_indexes(
                range(len(list_o_rooms))
            )

            salt = GeneticTreeShaker(
                adam,
                list_o_rooms
            )

            # g = SubdivideTreeToFloorplan(80, 60, list_o_rooms, adam)
            # fp = g.generate_candidate_floorplan()
            # renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')
            # input("[PAUSED]")

            for i in range(10):
                salt.run_generation()
                import statistics
                print(f"The best score so far is {statistics.median([tree.score for tree in salt.population])}")

            g = SubdivideTreeToFloorplan(80, 60, list_o_rooms, salt.population[0])
            fp = g.generate_candidate_floorplan()

            if salt.population[0].score > max_score:
                best_plan = fp
                max_score = salt.population[0].score
                renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')

        print("Max score was", max_score)
        return best_plan


