from bakedrandom import brandom as random
from evaluator.door_judge import DoorJudge
from recordclass import recordclass

DoorVectorScore = recordclass("DoorVectorScore", [
    "vector",
    "score"
])

class GeneticDoorShaker(object):

    def __init__(self, fp, initial_population, population_size=30, num_crossovers=30, prob_point_mutation=0.1):
        self.fp = fp
        self.population = [ DoorVectorScore(vector, 0) for vector in initial_population ]
        self.population_size = population_size
        self.prob_point_mutation = prob_point_mutation
        self.num_crossovers = num_crossovers

    def run_generation(self):
        candidates = self.crossover_population()
        self.mutate_candidates(candidates)
        self.score_candidates(candidates)
        self.population.extend(candidates)
        self.filter_population()

    def filter_population(self):
        self.population.sort(key=lambda node: node.score, reverse=True)
        # print([c.score for c in self.population])
        self.population = self.population[:self.population_size]

    def score_candidates(self, candidates):
        for candidate in candidates:
            dj = DoorJudge()
            self.fp.clear_doors()
            self.fp.add_doors(candidate.vector)

            cscore = dj.score_connectivity(self.fp)
            dscore = dj.score_individual_doors(self.fp)
            candidate.score = cscore + dscore

    def crossover_population(self):
        candidates = []
        for i in range(self.num_crossovers):
            a = random.choice(self.population)
            b = random.choice(self.population)
            c = self.crossover_individuals(a, b)
            candidates.append(c)
        return candidates

    def crossover_individuals(self, a, b):
        new_vector = []

        for i, j in zip(a.vector, b.vector):
            new_vector.append(random.choice([i, j]))

        return DoorVectorScore(
            vector=new_vector,
            score=0
        )

    def mutate_candidates(self, candidates):
        for candidate in candidates:
            self.mutate_individual(candidate)

    def mutate_individual(self, candidate):
        for i in range(len(candidate.vector)):
            if random.random() < self.prob_point_mutation:
                candidate.vector[i] = 1 - candidate.vector[i]
