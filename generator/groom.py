import random
import string

class Groom(object):

    def __init__(self, area, label):
        self.area = area
        self.label = label + "_" + str(random.randint(0, 999))

    def tree_score(self, actual_room):
        return 1.0

    def door_score(self, actual_room):
        return 1.0


class LivingGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Living")


class DiningGroom(LivingGroom):
    pass


class KitchenGroom(LivingGroom):
    pass


class BedGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Bedroom")

    def tree_score(self, actual_room):
        return min(0.5, actual_room.min_aspect_ratio) / 0.5

    def door_score(self, actual_room):
        door_counter = 0
        multiplier = 1
        for neighbor, edge in actual_room.neighbors_and_edges:
            if len(edge.doors) == 0:
                continue

            # Don't penalize bathgrooms
            if type(neighbor.groom) is BathGroom:
                continue

            # Penalize bedroom to bedroom
            if type(neighbor.groom) is BedGroom:
                multiplier = 0.1

            door_counter += len(edge.doors)
            if edge.opposite_room(actual_room) is None and len(edge.doors) > 0:
                multiplier = 0.1

        if door_counter == 0:
            return 0
        return multiplier / door_counter


class BathGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Bath")

    def tree_score(self, actual_room):
        return min(0.75, actual_room.min_aspect_ratio) / 0.75

    def door_score(self, actual_room):
        door_counter = 0
        multiplier = 1
        for edge in actual_room.edges:
            door_counter += len(edge.doors)
            if edge.opposite_room(actual_room) is None and len(edge.doors) > 0:
                multiplier = 0.25

        if door_counter == 0:
            return 0
        return multiplier / door_counter



