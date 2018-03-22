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

def load_floorplan(filename):
    with open(filename + ".pickle", 'rb') as f:
        dna = pickle.load(f)
        return dna


class FloorplanEvaluator(object):

    def __init__(self):  # TODO: Pass weights into here
        pass

    def score_floorplan(self, floorplan):
        scores = [ room.groom.tree_score(room) for room in floorplan.rooms ]
        room_scores = [ (1 - score)**2 for score in scores if score is not None]
        mean_score = sum(room_scores) / len(room_scores)
        return 1 - mean_score

    def score_tree(self, rootnode, list_o_rooms):
        if len(rootnode.children) <= 1:
            groom = list_o_rooms[rootnode.room_indexes[0]]
            return rootnode.score

        child_scores = []
        for child in rootnode.children:
            child_scores.append(self.score_tree(child, list_o_rooms))

        rootnode.score = min(child_scores)
        return rootnode.score


class PopulationCentrifuge(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        pass

    def dump_plan(self, fp, door_vector, generation_num, list_o_rooms, width, height, rootnode):
        fp.clear_doors()
        fp.add_doors(door_vector)

        filename = f"out/floorplan-{generation_num}"
        save_floorplan(FloorplanDNA(
                list_o_rooms=list_o_rooms,
                width=width,
                height=height,
                rootnode=rootnode,
                door_vector=door_vector
            ),
            fp,
            filename,
        )
        renderer.svgrenderer.SvgRenderer(fp, width, height).render(filename + '.svg', show_edge_connections=False)

    def create_perfect_floorplan(self):
        max_score = float('-inf')
        best_plan = None

        width = self.width
        height = self.height

        for generation in range(1):
            print("We are evaluating population ", generation)

            list_o_rooms = [BedGroom(2), BathGroom(1)] + [LivingGroom(4), BedGroom(2.25), BathGroom(1), BedGroom(2)]
            list_o_rooms = list(itertools.chain(list_o_rooms*10))

            adam = SubdivideTreeGenerator().generate_tree_from_indexes(
                range(len(list_o_rooms))
            )

            instantiator = SubdivideTreeToFloorplan(width, height, list_o_rooms)

            salt = GeneticTreeShaker(
                adam,
                list_o_rooms,
                instantiator,
                FloorplanEvaluator(),
            )

            for i in range(500):
                salt.run_generation()
                import statistics
                print(f"The best score so far is {max([tree.score for tree in salt.population])}")

                fp = instantiator.generate_candidate_floorplan(salt.population[0])

                # Check the doors
                # shaker = GeneticDoorShaker(fp, [ RandomDoorGenerator.create_door_vector(len(fp.edges)) for i in range(20)])
                # for j in range(200):
                #     shaker.run_generation()


                composite_score = salt.population[0].score
                door_vector = [0]*len(fp.edges)

                if composite_score > max_score:
                    best_plan = fp, door_vector
                    max_score = composite_score

                    self.dump_plan(
                        fp,
                        door_vector,
                        i,
                        list_o_rooms,
                        width, height,
                        salt.population[0],
                    )

                # renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')

        print("Max score was", max_score)

        fp, vector = best_plan
        fp.clear_doors()
        fp.add_doors(vector)

        return fp


