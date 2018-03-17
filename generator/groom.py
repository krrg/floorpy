from bakedrandom import brandom as random
import string

class Groom(object):

    def __init__(self, area, label):
        self.area = area
        self.label = label + "_" + str(random.randint(0, 999))

    def tree_score(self, actual_room):
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

    def tree_score(self, actual_room):
        return min(0.5, actual_room.min_aspect_ratio) / 0.5


class DiningGroom(LivingGroom):

    def __init__(self, area):
        super().__init__(area, "Living")


class KitchenGroom(LivingGroom):
    pass


class HallwayGroom(Groom):

    def __init__(self):
        super().__init__(0, "Hallway")

    def tree_score(self, actual_room):
        thin_edge_length = min(actual_room.height, actual_room.width)
        if thin_edge_length < 7:
            return (0.1 * thin_edge_length) / 6.0
        elif thin_edge_length > 8:
            return 1.0 / (thin_edge_length - 8)
        else:
            return 1.0


class BedGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Bedroom")

    def tree_score(self, actual_room):
        multiplier = 1.0
        non_bedgrooms = 0

        for neighbor, edge in actual_room.neighbors_and_edges:
            if type(neighbor.groom) is not BedGroom:
                non_bedgrooms += 1

        if non_bedgrooms == 0:
            multiplier = 0.1

        return multiplier * min(0.5, actual_room.min_aspect_ratio) / 0.5

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



