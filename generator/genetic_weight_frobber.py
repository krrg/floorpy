from bakedrandom import brandom as random
from generator.tree_judge import FloorplanEvaluator
from generator.groom import TreeWeights
import numpy as np

from multiprocessing import Pool


# https://stackoverflow.com/questions/34968722
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


class GeneticWeightFrobber(object):

    def __init__(self,
        initial_weights,
        fp_pairs,
    ):
        self.fp_pairs = fp_pairs
        self.population = [(initial_weights, (0, float('inf')))]
        self.prob_point_mutation = 0.5
        self.prob_inherit_from_b = 0.25
        self.num_candidates = 100
        self.population_size = 40

    def run_generation(self):
        candidates = self.crossover_population()
        candidates = self.mutate_candidates(candidates)
        scored_candidates = self.score_candidates(candidates)
        self.cull_herd(scored_candidates)

    def crossover_population(self):
        candidates = []
        population = [ w for w, score in self.population ]
        for i in range(self.num_candidates):
            a = random.choice(population)
            b = random.choice(population)
            c = self.crossover_weights(a, b)
            candidates.append(c)
        return candidates

    def crossover_weights(self, a, b):
        child = dict(a)
        for key in a.keys():
            if random.random() < self.prob_inherit_from_b:
                child[key] = b[key]
        return child

    def mutate_candidates(self, candidates):
        return [ self.mutate_individual(w) for w in candidates ]

    def mutate_individual(self, weights):
        mutant = dict(weights)
        for key in weights.keys():
            if random.random() <= self.prob_point_mutation:
                mutant[key] += random.uniform(-0.3, 0.3)
                mutant[key] = max(0.05, mutant[key])
        self.normalize_groom_weights(mutant)
        mutant["scoreCurveExponent"] = max(1, mutant["scoreCurveExponent"])
        return mutant

    def normalize_groom_weights(self, mutant):
        v = []
        keys = []

        for key in mutant.keys():
            if key.endswith("_weight"):
                keys.append(key)
                v.append(mutant[key])

        for normalized_weight, key in zip(softmax(np.array(v)), keys):
            mutant[key] = float(normalized_weight)

    def score_candidates(self, candidates):
        evaluator_candidates = [ FloorplanEvaluator(TreeWeights(**w)) for w in candidates ]
        with Pool(11) as p:
            scores = p.map(self.evaluate_candidate, evaluator_candidates)
            return zip(candidates, scores)

    def evaluate_candidate(self, evaluator):
        correct_count = 0
        accuracy = 0
        for good, bad in self.fp_pairs:
            good_score = evaluator.score_floorplan(good)
            bad_score = evaluator.score_floorplan(bad)
            # print("Good socre: ", good_score, " bad score"z, bad_score)
            if good_score >= bad_score:
                correct_count += 1
            # if bad_score >= good_score:
            accuracy += bad_score - good_score

        return -correct_count, accuracy,

    def cull_herd(self, candidates):
        self.population.extend(candidates)
        self.population.sort(key=lambda x: x[1])
        self.population = self.population[:self.population_size]








