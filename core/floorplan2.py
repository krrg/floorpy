import numpy as np
from core.edge import Orientation

class FloorPlan2(object):

    def __init__(self, rooms):
        self.rooms = rooms

    def subdivide(self, x, y, direction):

        p = np.array([x,y])

        if direction == Orientation.Horizontal:
            direction = np.array([1,0])
        else:
            direction = np.array([0,1])

        success = False
        for room in self.rooms:
            if not room.contains(p):
                continue
            roomA, roomB = room.subdivide(p, direction)
            self.rooms.remove(room)
            self.rooms.append(roomA)
            self.rooms.append(roomB)
            break
