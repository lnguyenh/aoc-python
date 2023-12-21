from collections import deque, defaultdict

from utils.djikstra import djikstra
from utils.grid import Grid


class Garden(Grid):
    def __init__(self, lines):
        super().__init__(lines)
        self.start_point = self.get_start_point()
        self.dots = [key for key, value in self.grid.items() if value == "."]

    def get_start_point(self):
        for key, value in self.grid.items():
            if value == "S":
                return key

    def get_edges(self):
        edges = []
        for x0, y0 in self.dots:
            for x, y in [(x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)]:
                if self.grid.get((x, y)) in [".", "S"]:
                    edges.append(((x0, y0), (x, y), 1))
        return edges

    def step(self, n):
        edges = self.get_edges()
        distances = {}
        for dot in self.dots:
            distances[dot] = djikstra(edges, dot, self.start_point)[0]

        even_distances = [d for dot, d in distances.items() if d % 2 == 0 and d <= n]
        even_distances.append(self.start_point)

        return len(even_distances)


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    garden = Garden(lines)
    return garden.step(64)


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
