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
from generator.genetic_weight_frobber import GeneticWeightFrobber
from evaluator.door_judge import DoorJudge
from bakedrandom import brandom as random
import statistics
import matplotlib.pyplot as plt


def garbage_fire():

    weights = TreeWeights(**default_tree_weights)
    fp = PopulationCentrifuge(100, 80, weights).create_perfect_floorplan()
    # renderer.svgrenderer.SvgRenderer(fp, 100, 60).render('out/output.svg')


def get_floorplan(unfixed_filename):
    dna = load_floorplan("." + unfixed_filename.replace(".svg", ""))
    instantiator = SubdivideTreeToFloorplan(dna.width, dna.height, dna.list_o_rooms, TreeWeights(**default_tree_weights))
    fp = instantiator.generate_candidate_floorplan(dna.rootnode)
    return fp


def autofrob_tree_evaluator_weights():

    floorplan_pairs = []

    with open("./scores.txt") as f:
        lines = f.readlines()

        for line in lines:
            greater, lesser = line.split()
            floorplan_pairs.append((get_floorplan(greater), get_floorplan(lesser)))

    frobber = GeneticWeightFrobber(
        default_tree_weights,
        floorplan_pairs
    )

    for i in range(10000):
        print("Running a generation", i)
        frobber.run_generation()
        print(frobber.population[0])


if __name__ == "__main__":
    # main()
    # garbage_fire()
    autofrob_tree_evaluator_weights()

