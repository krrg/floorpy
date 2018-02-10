class FloorPlan(object):

    def __init__(self, rooms):
        self.rooms = rooms

    def subdivide(self, x, y, direction):

        success = False
        for room in self.rooms:
            if not room.contains(x, y):
                continue
            roomA, roomB = room.subdivide(x, y, direction)
            self.rooms.remove(room)
            self.rooms.append(roomA)
            self.rooms.append(roomB)
            break
