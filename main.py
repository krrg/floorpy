import renderer.svgrenderer
from core.room import RoomFactory, Room
from core.floorplan import FloorPlan
from core.edge import Orientation, Edge
import numpy as np
from generator.simple_generator import SimpleGenerator
from evaluator.composite_eval import CompositeEvaluator
from evaluator.basic_evals import *

def main():

    # room = RoomFactory.Rectangle(75 * 2, 20 *2)
    # fp = FloorPlan([room], scale=2)

    # fp.subdivide(20, 10, Orientation.Vertical)
    # fp.subdivide(33, 10, Orientation.Vertical)
    # fp.subdivide(30, 10, Orientation.Horizontal)
    # fp.subdivide(55, 15, Orientation.Horizontal)
    # fp.subdivide(33 + 11, 10, Orientation.Vertical)
    # fp.subdivide(75 - 11, 10, Orientation.Vertical)
    # fp.subdivide(50, 7, Orientation.Horizontal)



    # fp.subdivide(40, 40, Orientation.Horizontal)

    # fp.subdivide(20, 60, Orientation.Vertical)
    # fp.subdivide(20, 10, Orientation.Vertical)


    # fp.subdivide(30, 20, Orientation.Vertical)

    # fp.subdivide(60, 20, Orientation.Vertical)
    # fp.subdivide(80, 80, Orientation.Vertical)
    # fp.subdivide(60, 60, Orientation.Horizontal)
    # fp.subdivide(90, 60, Orientation.Horizontal)


    # roomA, roomB = room.subdivide(40, 40, Orientation.Horizontal)
    # roomB, roomC = roomB.subdivide(20, 60, Orientation.Vertical)
    # roomA, roomD = roomA.subdivide(30, 20, Orientation.Vertical)
    #
    # fp = FloorPlan([
    #     roomA, roomB, roomC, roomD
    # ])

    evaluator = CompositeEvaluator([
        DoorOffEdgeEvaluator(),
        MinimumWidthEvaluator(8),
        AdjacentHallwayFilter(),
        LongDeadEndFilter(),
        LowMeanAreaPerimeterRatio(),
    ])

    rooms = 12
    width = rooms * 10
    height = int(rooms * 7.5)

    sg = SimpleGenerator(width, height, range(rooms))

    for i, fp in enumerate(sg.generate_candidate_floorplan()):
        print(f"Evaluating {i}")
        
        if evaluator.evaluate(fp) >= len(evaluator.evaluators):
            print("My score is ", evaluator.evaluate(fp))
            break
        
    renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')


if __name__ == "__main__":
    main()
