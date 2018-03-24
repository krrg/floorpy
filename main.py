import renderer.svgrenderer
from core.room import RoomFactory, Room
from core.floorplan import FloorPlan
from core.edge import Orientation, Edge
import numpy as np
from generator.simple_generator import SimpleGenerator
from evaluator.composite_eval import CompositeEvaluator
from evaluator.basic_evals import *
from generator.genetic_tree_shaker import GeneticTreeShaker
from generator.subdivide_tree_generator import *
from generator.groom import *
from generator.tree_judge import PopulationCentrifuge, load_floorplan, FloorplanEvaluator
from generator.random_door_generator import RandomDoorGenerator
from generator.genetic_door_shaker import GeneticDoorShaker
from evaluator.door_judge import DoorJudge
from bakedrandom import brandom as random


def garbage_fire():

    weights = TreeWeights(**default_tree_weights)
    fp = PopulationCentrifuge(100, 80, weights).create_perfect_floorplan()
    # renderer.svgrenderer.SvgRenderer(fp, 100, 60).render('out/output.svg')


def autofrob_tree_evaluator_weights():
    dna = load_floorplan("out/floorplan-1")
    weights = TreeWeights(**default_tree_weights)

    weights.scoreCurveExponent = 9

    instantiator = SubdivideTreeToFloorplan(dna.width, dna.height, dna.list_o_rooms, weights)
    evaluator = FloorplanEvaluator(weights)

    fp = instantiator.generate_candidate_floorplan(dna.rootnode)
    print("here is the score, ", evaluator.score_floorplan(fp))

if __name__ == "__main__":
    # main()
    garbage_fire()
    # autofrob_tree_evaluator_weights()

