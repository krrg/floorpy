import renderer.svgrenderer
from core.room import RoomFactory, Room
from core.floorplan import FloorPlan

def main():
    fp = FloorPlan([
        RoomFactory.Rectangle(10, 12)
    ])

    renderer.svgrenderer.SvgRenderer.render_plan(fp)

if __name__ == "__main__":
    main()
