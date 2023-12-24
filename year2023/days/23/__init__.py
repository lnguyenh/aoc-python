from collections import defaultdict, deque

from utils.astar import astar
from utils.djikstra import djikstra
from utils.grid import Grid


def bfs(edges, start, destination):
    """
    Gets longest path from start to destination using BFS
    """

    # neighbours / graph
    neighbours = defaultdict(list)
    for from_node, to_node in edges:
        neighbours[from_node].append(to_node)

    # unique nodes
    nodes = set()
    for n1, n2 in edges:
        nodes.add(n1)
        nodes.add(n2)

    paths = deque([[start]])

    if start == destination:
        return 0, [start]

    max_path = 0

    while paths:
        path = paths.pop()
        node = path[-1]

        # Getting the neighbours could be made dynamic for some aoc problems
        # based on problem rules instead of hardcoded list of edges
        for neighbour in neighbours[node]:
            if neighbour in path:
                continue
            new_path = list(path)
            new_path.append(neighbour)

            if neighbour == destination:
                max_path = max(max_path, len(path))
            else:
                paths.append(new_path)

    return max_path


class Hike(Grid):
    def __init__(self, lines):
        super().__init__(lines)
        self.start = (1, 0)
        self.stop = (self.maxx - 1, self.maxy)
        self.edges = self.build_edges()
        self.edges2 = self.build_edges2()

    def build_edges(self):
        edges = []
        for x0, y0 in self.points:
            v0 = self.grid.get((x0, y0))
            for i, (x, y) in enumerate(
                [(x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)]
            ):
                v1 = self.grid.get((x, y))
                if v1 is None or v1 == "#":
                    continue
                if v0 == ">" and i != 0:
                    continue
                if v0 == "<" and i != 1:
                    continue
                if v0 == "v" and i != 2:
                    continue
                if v0 == "^" and i != 3:
                    continue
                edges.append(((x0, y0), (x, y), -1))
        return edges

    def build_edges2(self):
        edges = []
        for x0, y0 in self.points:
            for i, (x, y) in enumerate(
                [(x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)]
            ):
                v1 = self.grid.get((x, y))
                if v1 is None or v1 == "#":
                    continue
                edges.append(((x0, y0), (x, y), -1))
        return edges


def process_input(blob):
    return blob.split("\n")


def do_part_1(processed_input):
    lines = processed_input
    hike = Hike(lines)
    return djikstra(hike.edges, hike.start, hike.stop)


def do_part_2(processed_input):
    lines = processed_input
    hike = Hike(lines)
    return -astar(hike.edges2, hike.start, hike.stop)[0]


def do_visualization(processed_input):
    return None
