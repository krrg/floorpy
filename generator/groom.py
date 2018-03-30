from bakedrandom import brandom as random
import string
from recordclass import recordclass
from core.edge import Orientation

default_tree_weights = {
    'Living_aspectRatioCap': 0.5,
    'Hallway_fourNeighbors': 0.65,
    'Bedroom_nonBedroomMultiplier': 0.1,
    'Bedroom_aspectRatioCap': 0.5,
    'Bathroom_aspectRatioCap': 0.75,
    'LivingGroom_weight': 1.0,
    'DiningGroom_weight': 1.0,
    'KitchenGroom_weight': 1.0,
    'HallwayGroom_weight': 1.0,
    'BedGroom_weight': 1.0,
    'BathGroom_weight': 1.0,
    'BedGroom_splittingHouseBlockerMultiplier': 0.1,
    'scoreCurveExponent': 2.0,
}

# default_tree_weights = {'Living_aspectRatioCap': 0.1821683604152357, 'Hallway_fourNeighbors': 0.3387275342787624, 'Bedroom_nonBedroomMultiplier': 0.6030077217720116, 'Bedroom_aspectRatioCap': 0.6295374742768074, 'Bathroom_aspectRatioCap': 1.3133567117389542, 'LivingGroom_weight': 0.1610819840974928, 'DiningGroom_weight': 0.160103699429546, 'KitchenGroom_weight': 0.14363177974131605, 'HallwayGroom_weight': 0.15812435712055573, 'BedGroom_weight': 0.21617087013841702, 'BathGroom_weight': 0.1608873094726724, 'scoreCurveExponent': 4.806756928566799}

TreeWeights = recordclass('TreeWeights', default_tree_weights.keys())


class Groom(object):

    def __init__(self, area, label):
        self.area = area
        self.label = label + "_" + str(random.randint(0, 999))

    def tree_score(self, actual_room, weights):
        return 1.0

    def door_score(self, actual_room):
        return 1.0

    def tree_weight(self, weights):
        return 0

class JiltedGroom(Groom):

    def __init__(self):
        super().__init__(0, "Jilted :(")

    def tree_score(self, actual_room, weights):
        return 0.0

    def door_score(self, actual_room):
        return 0.0


class LivingGroom(Groom):

    def __init__(self, area, label=None):
        super().__init__(area, label or "Living")

    def tree_weight(self, weights):
        return weights.LivingGroom_weight

    def tree_score(self, actual_room, weights):
        aspectRatioCap = weights.Living_aspectRatioCap
        return min(aspectRatioCap, actual_room.min_aspect_ratio) / aspectRatioCap


class DiningGroom(LivingGroom):

    def __init__(self, area):
        super().__init__(area, label="Dining")

    def tree_weight(self, weights):
        return weights.DiningGroom_weight

    # def tree_score(self, actual_room, weights):
    #     return

class KitchenGroom(LivingGroom):

    def __init__(self, area):
        super().__init__(area, label="Kitchen")

    def tree_weight(self, weights):
        return weights.KitchenGroom_weight

class HallwayGroom(Groom):

    def __init__(self):
        super().__init__(0, "Hallway")

    def tree_weight(self, weights):
        return weights.HallwayGroom_weight

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

        is_blocking = False

        if not (actual_room.has_one_none_neighbor(Orientation.Vertical) and actual_room.has_one_none_neighbor(Orientation.Horizontal)):
            for orientation in [Orientation.Vertical, Orientation.Horizontal]:
                if actual_room.has_one_none_neighbor(orientation):
                    print("I have only one none neighbor ", actual_room, actual_room.area)
                    for neighbor, edge in actual_room.neighbors_and_edges:
                        if type(neighbor.groom) is BathGroom or type(neighbor.groom) is BedGroom:
                            if edge.orientation == orientation:
                                if neighbor.has_one_none_neighbor(orientation):
                                    print("My name is ", actual_room, actual_room.area, " and I am blocking with ", neighbor, neighbor.area, " with a between edge of ", edge.orientation)
                                    is_blocking = True
                                    break

        if is_blocking:
            multiplier *= weights.BedGroom_splittingHouseBlockerMultiplier

        return multiplier * min(weights.Bedroom_aspectRatioCap, actual_room.min_aspect_ratio) / weights.Bedroom_aspectRatioCap

    def tree_weight(self, weights):
        return weights.BedGroom_weight

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

    def tree_weight(self, weights):
        return weights.BathGroom_weight

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





