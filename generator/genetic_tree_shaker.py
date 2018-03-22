from bakedrandom import brandom as random
from generator.node import Node
from generator.subdivide_tree_generator import *
import copy
from multiprocessing import Pool


class GeneticTreeShaker(object):

    def __init__(self,
            adam,
            list_o_rooms,
            fp_instantiator,
            fp_evaluator,
            population_size=15,
            num_crossovers=30,
            prob_orientation_mutates=0.35,
            prob_order_mutates=0.35,
            prob_t_mutates=0.2,
            prob_padding_mutates=0.1,
            t_mutation_magnitude=0.1
        ):

        adam.score = 0
        self.population_size = population_size
        self.num_crossovers = num_crossovers
        self.population = [ adam ]
        self.list_o_rooms = list_o_rooms
        self.prob_order_mutates = prob_order_mutates
        self.prob_orientation_mutates = prob_orientation_mutates
        self.prob_padding_mutates = prob_padding_mutates
        self.fp_instantiator = fp_instantiator
        self.fp_evaluator = fp_evaluator
        self.prob_t_mutates = prob_t_mutates
        self.t_mutation_magnitude = t_mutation_magnitude


    def list_nodes(self, candidate):
        nodes = [candidate]
        for child in candidate.children:
            nodes.extend(self.list_nodes(child))
        return nodes

    def run_generation(self):
        candidates = self.crossover_population()
        self.mutate_candidates(candidates)
        self.score_candidates(candidates)
        self.population.extend(candidates)
        self.filter_population()

    def filter_population(self):
        self.population.sort(key=lambda node: node.score, reverse=True)
        self.population = self.population[:self.population_size]

    def score_candidates(self, candidates):
        with Pool(11) as p:
            scores = p.map(self.score_candidate_subprocess, candidates)
            for candidate, score in zip(candidates, scores):
                candidate.score = score

        # for candidate in candidates:
        #     fp = self.fp_instantiator.generate_candidate_floorplan(candidate)
        #     candidate.score = self.fp_evaluator.score_floorplan(fp)

    def score_candidate_subprocess(self, candidate):
        fp = self.fp_instantiator.generate_candidate_floorplan(candidate)
        return self.fp_evaluator.score_floorplan(fp)

    def crossover_population(self):
        candidates = []
        for i in range(self.num_crossovers):
            a = random.choice(self.population)
            b = random.choice(self.population)
            c = self.crossover_individuals(a, b)
            candidates.append(c)
        return candidates

    def crossover_individuals(self, a, b):
        a, b = copy.deepcopy(a), copy.deepcopy(b)
        nodesA = self.list_nodes(a)
        nodesB = self.list_nodes(b)

        assert len(nodesA) == len(nodesB)

        random_indexes = range(0, len(nodesA))
        weights = [ 1 - node.score if node.score else 1 for node in nodesA ]
        random_index = weighted_choice(list(zip(random_indexes, weights)))

        subtreeA = nodesA[random_index]
        subtreeB = nodesB[random_index]

        subtreeA.orientation = subtreeB.orientation
        subtreeA.children = subtreeB.children
        subtreeA.padding = subtreeB.padding
        subtreeA.order = subtreeB.order
        subtreeA.t = subtreeB.t

        return a
        # for achild, bchild in zip(a.children, b.children):
        #     child.children.append(self.crossover_individuals(achild, bchild))
        # return child

    def mutate_candidates(self, candidates):
        for candidate in candidates:
            nodes = self.list_nodes(candidate)

            weights = [ 1 - node.score if node.score else 1 for node in nodes ]
            rand_node = weighted_choice(list(zip(nodes, weights)))

            self.mutate_individual(rand_node)

    def mutate_individual(self, candidate):
        if random.random() < self.prob_order_mutates:
            candidate.order *= -1
        if random.random() < self.prob_orientation_mutates:
            candidate.orientation = candidate.orientation.negate()
        # if random.random() < self.prob_t_mutates:
        #     candidate.t += random.uniform(-self.t_mutation_magnitude, self.t_mutation_magnitude)
        if random.random() < self.prob_padding_mutates:
            candidate.padding = not candidate.padding

        candidate.t = min(max(candidate.t, 0.3), 0.7)

        for child in candidate.children:
            self.mutate_individual(child)



# https://stackoverflow.com/questions/3679694
def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

