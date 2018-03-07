import copy
from bakedrandom import brandom as random
from generator.node import Node
from generator.subdivide_tree_generator import *

class GeneticTreeShaker(object):

    def __init__(self,
            adam,
            list_o_rooms,
            population_size=15,
            num_crossovers=40,
            prob_orientation_mutates=0.4,
            prob_order_mutates=0.4,
        ):

        adam.score = 0
        self.population_size = population_size
        self.num_crossovers = num_crossovers
        self.population = [ adam ]
        self.list_o_rooms = list_o_rooms
        self.prob_order_mutates = prob_order_mutates
        self.prob_orientation_mutates = prob_orientation_mutates

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
            g = SubdivideTreeToFloorplan(80, 60, self.list_o_rooms, candidate)
            fp = g.generate_candidate_floorplan()

    def crossover_population(self):
        candidates = []
        for i in range(self.num_crossovers):
            a = random.choice(self.population)
            b = random.choice(self.population)
            c = self.crossover_individuals(a, b)
            candidates.append(c)
        return candidates

    def crossover_individuals(self, a, b):
        child = Node(
            orientation=random.choice([a.orientation, b.orientation]),
            children=[],
            padding=random.choice([a.padding, b.padding]),
            order=random.choice([a.order, b.order]),
            t=random.choice([a.t, b.t]),  # TODO: This actually needs to flip with the order
            room_indexes=list(a.room_indexes),
            score=None,
        )

        for achild, bchild in zip(a.children, b.children):
            child.children.append(self.crossover_individuals(achild, bchild))
        return child

    def mutate_candidates(self, candidates):
        for candidate in candidates:
            self.mutate_individual(candidate)

    def mutate_individual(self, candidate):
        if random.random() < self.prob_order_mutates:
            candidate.order *= -1
        if random.random() < self.prob_orientation_mutates:
            candidate.orientation = candidate.orientation.negate()

        for child in candidate.children:
            self.mutate_individual(child)

