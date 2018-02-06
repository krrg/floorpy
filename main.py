import renderer.svgrenderer
from core.room import RoomFactory, Room
from core.floorplan import FloorPlan
from core.edge import Orientation

def main():

    room = RoomFactory.Rectangle(10, 12)

    roomA, roomB = room.subdivide(4, 4, Orientation.Horizontal)
    roomB, roomC = roomB.subdivide(2, 6, Orientation.Vertical)
    roomA, roomD = roomA.subdivide(2, 2, Orientation.Vertical)

    fp = FloorPlan([
        roomA, roomB, roomC, roomD
    ])

    renderer.svgrenderer.SvgRenderer.render_plan(fp)

if __name__ == "__main__":
    main()
