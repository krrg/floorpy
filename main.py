import renderer.svgrenderer
from core.room import RoomFactory, Room
from core.floorplan2 import FloorPlan2
from core.edge import Orientation

from core.edge2 import Edge2
from core.room2 import Room2
import numpy as np

def main():

    # room = RoomFactory.Rectangle(100, 120)
    p0 = np.array([0  ,0])
    p1 = np.array([100,0])
    p2 = np.array([100,120])
    p3 = np.array([0,120])

    edges = [Edge2(p0, p1), Edge2(p1, p2), Edge2(p2,p3), Edge2(p3,p0)]
    room = Room2(edges)

    for e in edges:
        e.positive = room


    fp = FloorPlan2([room])

    fp.subdivide(40, 40, Orientation.Horizontal)

    fp.subdivide(20, 60, Orientation.Vertical)
    fp.subdivide(20, 10, Orientation.Vertical)


    # fp.subdivide(30, 20, Orientation.Vertical)
    #
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



    renderer.svgrenderer.SvgRenderer.render_plan(fp, connectivity_graph=True)

if __name__ == "__main__":
    main()
