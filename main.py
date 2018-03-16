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
from generator.tree_judge import TreeJudge
from generator.random_door_generator import RandomDoorGenerator
from generator.genetic_door_shaker import GeneticDoorShaker
from evaluator.door_judge import DoorJudge
from bakedrandom import brandom as random

def garbage_fire_2():

    list_o_rooms = [BedGroom(2), BedGroom(2), LivingGroom(4), DiningGroom(1)]
    adam = SubdivideTreeGenerator().generate_tree_from_indexes(
        range(len(list_o_rooms))
    )
    instantiator = SubdivideTreeToFloorplan(80, 60, list_o_rooms)
    fp = instantiator.generate_candidate_floorplan(adam)

    renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')


def garbage_fire():

    fp = TreeJudge().create_perfect_floorplan()



    # door_vector = RandomDoorGenerator.create_door_vector(len(fp.edges))
    # fp.add_doors(door_vector)

    renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')

if __name__ == "__main__":
    # main()
    garbage_fire()
