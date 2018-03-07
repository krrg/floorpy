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

def garbage_fire():

    fp = TreeJudge().create_perfect_floorplan()
    RandomDoorGenerator.ran


    renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')

if __name__ == "__main__":
    # main()
    garbage_fire()
