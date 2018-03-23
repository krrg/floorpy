from bakedrandom import brandom as random
import string
from recordclass import recordclass

default_tree_weights = {
    'Living_aspectRatioCap': 0.5,
    'Hallway_fourNeighbors': 0.65,
    'Bedroom_nonBedroomMultiplier': 0.1,
    'Bedroom_aspectRatioCap': 0.5,
    'Bathroom_aspectRatioCap': 0.75,
}

TreeWeights = recordclass('TreeWeights', default_tree_weights.keys())


class Groom(object):

    def __init__(self, area, label):
        self.area = area
        self.label = label + "_" + str(random.randint(0, 999))

    def tree_score(self, actual_room, weights):
        return 1.0

    def door_score(self, actual_room):
        return 1.0

class JiltedGroom(Groom):

    def __init__(self):
        super().__init__(0, "Jilted :(")

    def tree_score(self, actual_room):
        return 0.0

    def door_score(self, actual_room):
        return 0.0


class LivingGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Living")

    def tree_score(self, actual_room, weights):
        aspectRatioCap = weights.Living_aspectRatioCap
        return min(aspectRatioCap, actual_room.min_aspect_ratio) / aspectRatioCap


class DiningGroom(LivingGroom):

    def __init__(self, area):
        super().__init__(area, "Living")


class KitchenGroom(LivingGroom):
    pass


class HallwayGroom(Groom):

    def __init__(self):
        super().__init__(0, "Hallway")

    def tree_score(self, actual_room, weights):
        # return None

        # Scored on the basis of how many non-hallway neighbors it has.
        non_hall_neighbors = 0
        for neighbor, edge in actual_room.neighbors_and_edges:
            if edge.length < 8:
                continue
            if type(neighbor.groom) is HallwayGroom:
                continue
            non_hall_neighbors += 1

        if non_hall_neighbors >= 5:
            return None
        elif non_hall_neighbors == 4:
            return weights.Hallway_fourNeighbors
        elif non_hall_neighbors <= 3:
            return 0



class BedGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Bedroom")

    def tree_score(self, actual_room, weights):
        multiplier = 1.0
        non_bedgrooms = 0

        for neighbor, edge in actual_room.neighbors_and_edges:
            if type(neighbor.groom) is not BedGroom:
                non_bedgrooms += 1

        if non_bedgrooms == 0:
            multiplier = weights.Bedroom_nonBedroomMultiplier

        return multiplier * min(weights.Bedroom_aspectRatioCap, actual_room.min_aspect_ratio) / weights.Bedroom_aspectRatioCap

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

    def tree_score(self, actual_room, weights):
        return min(weights.Bathroom_aspectRatioCap, actual_room.min_aspect_ratio) / weights.Bathroom_aspectRatioCap

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



