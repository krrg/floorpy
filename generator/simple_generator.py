from core.floorplan import FloorPlan
from core.room import RoomFactory
from collections import deque
import random
import math
from core.edge import Orientation
from core.opening import DoorFactory
from collections import deque


class SimpleGenerator(object):

    def __init__(self, lot_width, lot_height, list_o_rooms):
        self.lot_width = lot_width
        self.lot_height = lot_height
        self.desired_rooms = list_o_rooms

    def get_largest_room(self, rooms):
        return max(rooms, key=lambda r: r.area)

    def get_random_point_in_room(self, room):
        x, y = room.center
        std_dev = 0.15 * int(math.sqrt(room.area))

        rx = int(random.gauss(x, std_dev))
        ry = int(random.gauss(y, std_dev))

        return rx, ry

    def get_nearest_value(self, x, search_radius, used_set):
        for i in range(search_radius):
            if x + i in used_set:
                return x + i
            if x - i in used_set:
                return x - i
        return x        

    def generate_candidate_floorplan(self):
        used_rx = set()
        used_ry = set()

        while True:
            floorplan = FloorPlan([RoomFactory.Rectangle(self.lot_width, self.lot_height)])
            while len(floorplan.rooms) < len(self.desired_rooms):
                largest = self.get_largest_room(floorplan.rooms)

                while True:
                    rx, ry = self.get_random_point_in_room(largest)

                    corrected_rx = self.get_nearest_value(rx, 6, used_rx)
                    corrected_ry = self.get_nearest_value(ry, 6, used_ry)

                    used_rx.add(corrected_rx)
                    used_ry.add(corrected_ry)

                    if largest.contains((corrected_rx, corrected_ry)):
                        break
                floorplan.subdivide(corrected_rx, corrected_ry, random.choice([Orientation.Horizontal, Orientation.Vertical]))

            self.add_doors(floorplan)

            yield floorplan

    def add_doors(self, floorplan):
        visited_rooms = set([floorplan.rooms[0]])

        # pick starter room
        stack = deque([floorplan.rooms[0]])
        while len(visited_rooms) < len(floorplan.rooms):
            current = stack.popleft()
            for neighbor, edge in current.neighbors_and_edges:
                if neighbor in visited_rooms:
                    continue
                a, b = edge.t_bounds(4)
                if a is None:
                    continue

                edge.doors.append(
                    DoorFactory.interior_door(random.uniform(a, b), random.choice([-1, 1]))
                )

                visited_rooms.add(neighbor)
                stack.append(neighbor)


            # visited_rooms.add(current)
            # stack.extend(current.neighbors)






