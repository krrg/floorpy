import scipy.sparse.csgraph
import numpy as np
from core.floorplan import FloorPlan
from core.room import RoomFactory
from collections import deque
from bakedrandom import brandom as random
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
                # print(f"Was going to do {x} but corrected to {x + i}")
                return x + i
            if x - i in used_set:
                # print(f"Was going to do {x} but corrected to {x - i}")
                return x - i
        return x

    def generate_candidate_floorplan(self):

        while True:
            used_rx = set()
            used_ry = set()

            floorplan = FloorPlan([RoomFactory.Rectangle(self.lot_width, self.lot_height)])
            while len(floorplan.rooms) < len(self.desired_rooms):
                largest = self.get_largest_room(floorplan.rooms)

                while True:
                    rx, ry = self.get_random_point_in_room(largest)

                    correction_radius = 9
                    corrected_rx = self.get_nearest_value(rx, correction_radius, used_rx)
                    corrected_ry = self.get_nearest_value(ry, correction_radius, used_ry)

                    used_rx.add(corrected_rx)
                    used_ry.add(corrected_ry)

                    if largest.contains((corrected_rx, corrected_ry)):
                        break
                    else:
                        # Necessary to prevent infinite snap-to-grid loops
                        used_rx.add(rx)
                        used_ry.add(ry)

                floorplan.subdivide(corrected_rx, corrected_ry, random.choice([Orientation.Horizontal, Orientation.Vertical]))

            # self.add_doors_depth_first(floorplan)
            self.add_doors_minimum_spanning_tree(floorplan)

            yield floorplan

    def add_doors_depth_first(self, floorplan):
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

                side = random.choice([a, b])

                current_ap = (current.area / current.perimeter)
                neighbor_ap = (neighbor.area / neighbor.perimeter)

                direction = 1 if current_ap > neighbor_ap else -1

                edge.doors.append(
                    DoorFactory.interior_door(side, direction, "left" if side == b else "right")
                )

                visited_rooms.add(neighbor)
                stack.append(neighbor)

    def add_doors_minimum_spanning_tree(self, floorplan):

        matrix = np.full((len(floorplan.rooms), len(floorplan.rooms)), np.inf, dtype=np.float32)

        indexes = {}
        reverse_indexes = {}
        for i, room in enumerate(floorplan.rooms):
            indexes[room] = i
            reverse_indexes[i] = room

        for room in floorplan.rooms:
            for neighbor in room.neighbors:
                i = indexes[room]
                j = indexes[neighbor]
                matrix[i, j] = 1

        distances = scipy.sparse.csgraph.minimum_spanning_tree(matrix)
        # for di in distances:
            # print("Distance", di)
        for i, j in zip(*np.where(distances.toarray() == 1)):
            roomA = reverse_indexes[i]
            roomB = reverse_indexes[j]
            for neighbor, edge in roomA.neighbors_and_edges:
                if neighbor is roomB:
                    a, b = edge.t_bounds(4)
                    if a is None:
                        continue

                    side = random.choice([a, b])

                    current_ap = (roomA.area / roomA.perimeter)
                    neighbor_ap = (neighbor.area / neighbor.perimeter)

                    direction = 1 if current_ap > neighbor_ap else -1

                    edge.doors.append(
                        DoorFactory.interior_door(side, direction, "left" if side == b else "right")
                    )




            # visited_rooms.add(current)
            # stack.extend(current.neighbors)






