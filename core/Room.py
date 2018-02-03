class Room(object):

    def __init__(self):
        self.edges = []
        self.titles = []

    def area(self);
        return 0

    def is_complete(self):
        return len(self.titles) == 1

    def subdivide(self, x, direction):
        pass # should return two new rooms?
