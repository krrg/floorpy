class CompositeEvaluator(object):

    def __init__(self, evaluators):
        self.evaluators = evaluators

    def evaluate(self, floorplan):


        return sum([
            e.evaluate(floorplan) for e in self.evaluators
        ])
