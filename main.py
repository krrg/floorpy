import renderer.svgrenderer
from core.room import RoomFactory, Room
from core.floorplan import FloorPlan
from core.edge import Orientation

def main():

    room = RoomFactory.Rectangle(100, 120)

    roomA, roomB = room.subdivide(40, 40, Orientation.Horizontal)
    roomB, roomC = roomB.subdivide(20, 60, Orientation.Vertical)
    roomA, roomD = roomA.subdivide(30, 20, Orientation.Vertical)
    # roomA, roomE = roomA.subdivide(10, 10, Orientation.Horizontal)

    fp = FloorPlan([
        roomA, roomB, roomC, roomD
    ])

    renderer.svgrenderer.SvgRenderer.render_plan(fp, connectivity_graph=True)

if __name__ == "__main__":
    main()
