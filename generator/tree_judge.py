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

    def __init__(self, weights):
        self.weights = weights

    def score_floorplan(self, floorplan):
        scores = [ (room.groom.tree_score(room, self.weights), room.groom) for room in floorplan.rooms ]
        scores = [ (score, groom) for score, groom in scores if score is not None ]
        room_scores = [ (1 - score * groom.tree_weight(self.weights))**self.weights.scoreCurveExponent for score, groom in scores]
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

    def __init__(self, width, height, weights):
        self.width = width
        self.height = height
        self.weights = weights

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
        weights = self.weights

        for generation in range(100):
            print("We are evaluating population ", generation)

            # list_o_rooms = [LivingGroom(4), DiningGroom(2.5), KitchenGroom(2), BedGroom(1.9)]
            # list_o_rooms = []
            # list_o_rooms += [ BedGroom(1.9) ] * 71
            # list_o_rooms += [ LivingGroom(4.0) ] * 20
            # list_o_rooms += [ DiningGroom(2.5) ] * 20
            # list_o_rooms += [ CustomGroom(1.5, "Breakfast", "d3dfb8") ] * 15
            # list_o_rooms += [ CustomGroom(1.5, "Snacking", "f7a9a8") ] * 15
            # list_o_rooms += [ CustomGroom(1.5, "Standing", "717ec3") ] * 20
            # list_o_rooms += [ CustomGroom(5.0, "Ballroom", "b79ab7") ] * 10
            # list_o_rooms += [ BathGroom(1.0) ] * 20
            # list_o_rooms += [ KitchenGroom(2.0) ] * 20
            # list_o_rooms += [ CustomGroom(1.33, "No Purpose", "f7e1d7") ] * 30

            list_o_rooms = [LivingGroom(4), DiningGroom(2.5), KitchenGroom(2), BedGroom(1.8), BedGroom(1.8), BedGroom(2.0), BathGroom(1), BathGroom(1)]
            list_o_rooms = list(itertools.chain(list_o_rooms*1))

            adam = SubdivideTreeGenerator().generate_tree_from_indexes(
                range(len(list_o_rooms))
            )

            instantiator = SubdivideTreeToFloorplan(width, height, list_o_rooms, weights)

            salt = GeneticTreeShaker(
                adam,
                list_o_rooms,
                instantiator,
                FloorplanEvaluator(weights),
            )

            duplicate_score = 0
            max_score = 0
            for i in range(500):
                salt.run_generation()
                import statistics
                print(f"The best score so far is {max([tree.score for tree in salt.population])}")

                fp = instantiator.generate_candidate_floorplan(salt.population[0])

                # Check the doors
                composite_score = salt.population[0].score

                if composite_score == max_score:
                    duplicate_score += 1
                else:
                    duplicate_score = 0

                if duplicate_score >= 12:
                    break

                if composite_score > max_score:
                    import uuid
                    best_plan = fp, None
                    max_score = composite_score

            shaker = GeneticDoorShaker(fp, [ RandomDoorGenerator.create_door_vector(len(fp.edges)) for i in range(20)])
            for j in range(200):
                shaker.run_generation()
            door_vector = shaker.population[0].vector

            self.dump_plan(
                best_plan[0],
                door_vector,
                str(generation),
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


