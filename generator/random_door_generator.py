from bakedrandom import brandom as random

class RandomDoorGenerator(object):

    @staticmethod
    def create_door_vector(length):
        return [ random.choice([0, 1]) for i in range(length) ]
