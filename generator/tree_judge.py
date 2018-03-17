import generator.subdivide_tree_generator
from generator.groom import LivingGroom, BedGroom, BathGroom
import itertools
from generator.genetic_tree_shaker import GeneticTreeShaker
from generator.subdivide_tree_generator import *
from generator.groom import *
import renderer.svgrenderer
from generator.genetic_door_shaker import GeneticDoorShaker
from evaluator.door_judge import DoorJudge
from generator.random_door_generator import RandomDoorGenerator
from recordclass import recordclass
import pickle


FloorplanDNA = recordclass('FloorplanDNA', [
    'list_o_rooms',
    'width',
    'height',
    'rootnode',
    'door_vector',
])

def save_floorplan(dna, fp, filename):
    with open(filename + ".pickle", 'wb') as f:
        pickle.dump(dna, f)



class TreeJudge(object):

    def __init__(self):
        pass

    def create_perfect_floorplan(self):
        max_score = float('-inf')
        best_plan = None

        width = 80
        height = 60

        for generation in range(50):
            print("We are evaluating population ", generation)

            list_o_rooms = [BedGroom(2), BathGroom(1)] + [LivingGroom(4), BedGroom(2.25), BathGroom(1), BedGroom(2)]
            list_o_rooms = list(itertools.chain(list_o_rooms*1))

            adam = SubdivideTreeGenerator().generate_tree_from_indexes(
                range(len(list_o_rooms))
            )

            instantiator = SubdivideTreeToFloorplan(width, height, list_o_rooms)

            salt = GeneticTreeShaker(
                adam,
                list_o_rooms,
                instantiator
            )

            for i in range(5):
                salt.run_generation()
                import statistics
                print(f"The best score so far is {statistics.median([tree.score for tree in salt.population])}")

            fp = instantiator.generate_candidate_floorplan(salt.population[0])

            # Check the doors
            shaker = GeneticDoorShaker(fp, [ RandomDoorGenerator.create_door_vector(len(fp.edges)) for i in range(20)])
            for i in range(200):
                shaker.run_generation()


            composite_score = shaker.population[0].score + salt.population[0].score

            if composite_score > max_score:
                best_plan = fp, shaker.population[0].vector
                max_score = composite_score

                fp.clear_doors()
                fp.add_doors(shaker.population[0].vector)

                filename = f"out/floorplan-{generation}"
                save_floorplan(FloorplanDNA(
                        list_o_rooms=list_o_rooms,
                        width=width,
                        height=height,
                        rootnode=salt.population[0],
                        door_vector=shaker.population[0].vector
                    ),
                    fp,
                    filename,
                )
                renderer.svgrenderer.SvgRenderer(fp, width, height).render(filename + '.svg')
                # renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')

        print("Max score was", max_score)

        fp, vector = best_plan
        fp.clear_doors()
        fp.add_doors(vector)

        return fp


