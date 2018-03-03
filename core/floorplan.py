import numpy as np
from core.edge import Orientation

class FloorPlan(object):

    def __init__(self, rooms, scale=1):
        self.rooms = rooms
        self.scale = scale

    def subdivide(self, x, y, direction):

        p = np.array([x,y])
        p *= self.scale

        direction = direction.to_unit_vector()

        success = False
        for room in self.rooms:
            if not room.contains(p):
                continue
            roomA, roomB = room.subdivide(p, direction)
            self.rooms.remove(room)
            self.rooms.append(roomA)
            self.rooms.append(roomB)
            break

    def proportional_subdivide(self, S, direction, room):
        roomA, roomB = room.proportional_subdivide(S, direction)
        self.rooms.remove(room)
        self.rooms.append(roomA)
        self.rooms.append(roomB)
        return roomA, roomB
