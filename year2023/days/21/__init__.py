from collections import deque, defaultdict

from utils.djikstra import djikstra
from utils.grid import Grid


class Garden(Grid):
    def __init__(self, lines):
        super().__init__(lines)
        self.start_point = self.get_start_point()
        self.dots = [key for key, value in self.grid.items() if value == "."]
        self.hashtags = [key for key, value in self.grid.items() if value == "#"]
        self.distances = {}

    def get_start_point(self):
        for key, value in self.grid.items():
            if value == "S":
                return key

    def populate_distances(self):
        self.distances[self.start_point] = 0
        num_changes = 1
        while num_changes:
            num_changes = 0
            for x0, y0 in self.dots:
                neighbours = [(x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)]
                candidate_distances = [
                    self.distances.get(point)
                    for point in neighbours
                    if self.distances.get(point) is not None
                ]
                if candidate_distances:
                    distance = min(candidate_distances) + 1
                    if (x0, y0) not in self.distances or self.distances[
                        (x0, y0)
                    ] > distance:
                        self.distances[(x0, y0)] = distance
                        num_changes += 1
        toto = 1

    def do_part_1(self):
        self.populate_distances()
        even_distances = [
            d for dot, d in self.distances.items() if d % 2 == 0 and d <= 64
        ]
        return len(even_distances)

    def print_distances(self):
        x_min, x_max, y_min, y_max = self.get_min_maxes()
        for j in range(y_min, y_max + 1):
            line = ""
            for i in range(x_min, x_max + 1):
                c = self.distances.get((i, j), " # ")
                line += f"{c:<3}"
            print(line)
        print("\n")


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    garden = Garden(lines)
    return garden.do_part_1()


def do_part_2(lines):
    garden = Garden(lines)
    # garden.populate_distances()
    # garden.print_distances()
    return "toto"


def do_visualization(processed_input):
    return None
