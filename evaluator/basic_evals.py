class DoorOffEdgeEvaluator(object):

    def evaluate(self, floorplan):
        edgeset = set()
        for room in floorplan.rooms:
            for edge in room.edges:
                edgeset.add(edge)

        for edge in edgeset:
            for door in edge.doors:
                a, b = edge.radial_t_values(door.t, door.width / 2)
                for t in [a, b]:
                    if t <= 0 or t >= 1:
                        print("Failed on t = ", t)
                        return 0
        return 1

class MinimumWidthEvaluator(object):

    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, floorplan):
        for room in floorplan.rooms:
            x_max, x_min, y_max, y_min = room.max_min_xy
            width = x_max - x_min
            height = y_max - y_min

            if width < self.threshold or height < self.threshold:
                return 0

        return 1
