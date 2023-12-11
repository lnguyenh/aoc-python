from itertools import combinations

from utils.grid import Grid


class Universe(Grid):
    def __init__(self, lines):
        super().__init__(lines)

    def detect_empty(self):
        minx, maxx, miny, maxy = self.get_min_maxes()
        row_indexes = set(range(maxy + 1))
        column_indexes = set(range(maxx + 1))
        for x, y in self.points:
            if self.grid[(x, y)] == "#":
                row_indexes.discard(y)
                column_indexes.discard(x)
        return list(row_indexes), list(column_indexes)

    def expand(self, delta):
        new_grid = {coordinates: c for coordinates, c in self.grid.items() if c == "#"}
        self.grid = new_grid

        j_expands, i_expands = self.detect_empty()
        galaxies = {
            coordinates: coordinates for i, coordinates in enumerate(self.grid.keys())
        }

        for i in i_expands:
            for (x0, y0), (x1, y1) in galaxies.items():
                if x0 > i:
                    galaxies[(x0, y0)] = (x1 + delta, y1)

        for j in j_expands:
            for (x0, y0), (x1, y1) in galaxies.items():
                if y0 > j:
                    galaxies[(x0, y0)] = (x1, y1 + delta)

        new_grid = {coordinates: "#" for _, coordinates in galaxies.items()}
        self.grid = new_grid

    def sum_shortest_paths(self):
        sum_paths = 0
        for (ax, ay), (bx, by) in list(combinations(self.grid.keys(), 2)):
            shortest_path = abs(bx - ax) + abs(by - ay)
            sum_paths += shortest_path
        return sum_paths


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    universe = Universe(lines)
    universe.expand(1)
    return universe.sum_shortest_paths()


def do_part_2(lines):
    universe = Universe(lines)
    universe.expand(999999)
    return universe.sum_shortest_paths()


def do_visualization(processed_input):
    return None
