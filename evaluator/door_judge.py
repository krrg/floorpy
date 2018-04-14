import generator.subdivide_tree_generator
from generator.groom import LivingGroom, BedGroom, BathGroom
import itertools
from generator.genetic_tree_shaker import GeneticTreeShaker
from generator.subdivide_tree_generator import *
from generator.groom import *
import renderer.svgrenderer
from generator.random_door_generator import RandomDoorGenerator
from collections import deque


class DoorJudge(object):

    def __init__(self):
        pass

    def score_connectivity(self, fp):
        islands = self.get_connectivity_islands(fp)
        largest_island = len(max(islands, key=lambda i: len(i)))
        connectivity_score = (largest_island / len(fp.rooms))**2
        connectivity_score *= 1.0 if self.outside_door_exists(fp) else 0.5
        return connectivity_score

    def score_individual_doors(self, fp):
        door_score = 0

        for room in fp.rooms:
            room_door_score = room.groom.door_score(room)**2
            door_score += room_door_score

        door_score /= len(fp.rooms)
        return door_score

    def outside_door_exists(self, fp):
        for edge in fp.edges:
            for door in edge.doors:
                if edge.positive is None or edge.negative is None:
                    return True
        return False

    def get_connectivity_islands(self, fp):
        rooms = set(fp.rooms)
        islands = []

        while len(rooms) > 0:
            r = rooms.pop()
            queue = deque([r])
            connected = []

            while len(queue) > 0:
                head = queue.popleft()
                connected.append(head)
                for neighbor, edge in head.neighbors_and_edges:
                    if len(edge.doors) > 0 and neighbor in rooms:
                        rooms.remove(neighbor)
                        queue.append(neighbor)

            islands.append(connected)

        return islands

    def create_perfect_doorplan(self, fp):
        max_score = float('-inf')
        best_door_vector = None

        for i in range(50000):

            fp.clear_doors()
            door_vector = RandomDoorGenerator.create_door_vector(len(fp.edges))
            fp.add_doors(door_vector)

            door_score = self.score_individual_doors(fp)
            connectivity_score = self.score_connectivity(fp) ** 2

            # if connectivity_score < 1.0:
                # print("Door score: ", door_score, " connectivity socre ", connectivity_score)


            composite_score = door_score + connectivity_score

            if composite_score > max_score:
                # print("Connectivity score is", connectivity_score, " door score ", door_score)
                best_door_vector = door_vector
                max_score = composite_score
                # renderer.svgrenderer.SvgRenderer(fp).render('out/output.svg')

            # print("The door score was", door_score, " current max is ", max_score)

        fp.clear_doors()
        fp.add_doors(best_door_vector)
        return fp


