from bakedrandom import brandom as random

class AbstractEdgeOpening(object):

    def __init__(self, t, width, opens_into):
        self.t = t
        self.width = width
        self.opens_into = opens_into  #


class Door(AbstractEdgeOpening):

    def __init__(self, t, width, opens_into, opens_LR):
        super().__init__(t, width, opens_into)
        self.opens_LR = opens_LR


class Window(AbstractEdgeOpening):
    pass


class DoorFactory(object):

    @staticmethod
    def interior_door(t, direction, left_or_right=None):
        return Door(t, 6, direction, left_or_right if left_or_right is not None else random.choice(["left", "right"]))

    @staticmethod
    def small_interior_door(t, direction):
        return Door(t, 5, direction, "left")

    @staticmethod
    def exterior_door(t, direction):
        return Door(t, 6, direction, "left")
