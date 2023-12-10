from collections import defaultdict

from utils.djikstra import djikstra
from utils.grid import Grid


class Maze(Grid):
    def __init__(self, lines):
        self.animal = None
        super().__init__(lines)
        self.edges = []
        self.links = defaultdict(list)
        self.create_edges()

    def populate_grid(self, lines):
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                self.set_grid_value(i, j, c)
                if c == "S":
                    self.animal = (i, j)

    def create_edges(self):
        for x, y in self.points:
            point = (x, y)
            c = self.grid[(x, y)]
            if c == "|":
                #
                self.edges.append((point, (x, y + 1), 1))
                self.edges.append(((x, y + 1), point, 1))
                #
                self.edges.append(((x, y - 1), point, 1))
                self.edges.append((point, (x, y - 1), 1))
                #
                self.links[point].append((x, y + 1))
                self.links[point].append((x, y - 1))
            elif c == "-":
                #
                self.edges.append((point, (x + 1, y), 1))
                self.edges.append(((x + 1, y), point, 1))
                #
                self.edges.append(((x - 1, y), point, 1))
                self.edges.append((point, (x - 1, y), 1))
                #
                self.links[point].append((x + 1, y))
                self.links[point].append((x - 1, y))
            elif c == "L":
                #
                self.edges.append((point, (x + 1, y), 1))
                self.edges.append(((x + 1, y), point, 1))
                #
                self.edges.append(((x, y - 1), point, 1))
                self.edges.append((point, (x, y - 1), 1))
                #
                self.links[point].append((x + 1, y))
                self.links[point].append((x, y - 1))
            elif c == "J":
                #
                self.edges.append((point, (x - 1, y), 1))
                self.edges.append(((x - 1, y), point, 1))
                #
                self.edges.append(((x, y - 1), point, 1))
                self.edges.append((point, (x, y - 1), 1))
                #
                self.links[point].append((x - 1, y))
                self.links[point].append((x, y - 1))
            elif c == "7":
                #
                self.edges.append((point, (x - 1, y), 1))
                self.edges.append(((x - 1, y), point, 1))
                #
                self.edges.append(((x, y + 1), point, 1))
                self.edges.append((point, (x, y + 1), 1))
                #
                self.links[point].append((x - 1, y))
                self.links[point].append((x, y + 1))
            elif c == "F":
                #
                self.edges.append((point, (x + 1, y), 1))
                self.edges.append(((x + 1, y), point, 1))
                #
                self.edges.append(((x, y + 1), point, 1))
                self.edges.append((point, (x, y + 1), 1))
                #
                self.links[point].append((x + 1, y))
                self.links[point].append((x, y + 1))

    def get_distance_to_animal(self, point):
        distance, path = djikstra(self.edges, self.animal, point)
        return distance, path

    def get_point_to(self, point_from, point_current):
        z = [point for point in self.links[point_current] if point != point_from]
        return z[0]

    def trace_loop(self):
        ax, ay = self.animal
        loop = []

        # find first point
        start = None
        for x, y in [(ax + 1, ay), (ax - 1, ay), (ax, ay - 1), (ax, ay + 1)]:
            if self.grid[(x, y)] in ["|", "-", "L", "J", "7", "F"]:
                start = (x, y)
                loop = [(ax, ay), (x, y)]
                break

        point_from = self.animal
        point_current = start
        while True:
            point_to = self.get_point_to(point_from, point_current)
            loop.append(point_to)
            if point_to == self.animal:
                break
            point_from = point_current
            point_current = point_to

        return len(loop), loop


def process_input(blob):
    lines = blob.split("\n")
    maze = Maze(lines)
    return maze


def do_part_1(maze):
    length, _ = maze.trace_loop()

    return int(round(length / 2))


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
