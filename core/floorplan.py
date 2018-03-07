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

    @property
    def edges(self):
        edge_list = list()
        edge_set = set()
        for room in self.rooms:
            for edge in room.edges:
                if edge in edge_set:
                    continue
                edge_list.append(edge)
                edge_set.add(edge)
        return edge_list

    def clear_doors(self):
        for room in self.rooms:
            for edge in room.edges:
                edge.doors = []

    def add_doors(self, door_vector):
        edge_list = self.edges

        if len(door_vector) != len(edge_list):
            raise Exception("Differing length of door vector and edges")

        for is_door, edge in zip(door_vector, edge_list):
            if is_door:
                a, b = edge.t_bounds(4)
                if a is None:
                    continue

                side = random.choice([a, b])
                direction = 1

                edge.doors.append(
                    DoorFactory.interior_door(side, direction, "left" if side == b else "right")
                )
