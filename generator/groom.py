import random
import string

class Groom(object):

    def __init__(self, area, label):
        self.area = area
        self.label = label + "_" + str(random.randint(0, 999))

    def score(self, actual_room):
        return 1.0


class LivingGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Living")


class BedGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Bedroom")

    def score(self, actual_room):
        return min(0.5, actual_room.min_aspect_ratio) / 0.5


class BathGroom(Groom):

    def __init__(self, area):
        super().__init__(area, "Bath")

    def score(self, actual_room):
        return min(0.75, actual_room.min_aspect_ratio) / 0.75



