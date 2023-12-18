from collections import deque

from utils.grid import Grid


DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "D": (0, 1),
    "U": (0, -1),
}


class Trench(Grid):
    def __init__(self, lines):
        super().__init__(lines)
        self.colors = {}

    def dig(self, instructions):
        x, y = (0, 0)
        self.grid[(x, y)] = "#"
        self.colors[(x, y)] = "1"
        for d, n, color in instructions:
            for _ in range(n):
                x += DIRECTIONS[d][0]
                y += DIRECTIONS[d][1]
                self.grid[(x, y)] = "#"
                self.colors[(x, y)] = color
        self.refresh_min_maxes()

    def get_neighbours(self, i, j):
        candidates = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [c for c in candidates if self.grid.get(c) == "."]

    def get_v(self):
        for i in range(self.minx - 2, self.maxx + 3):
            for j in range(self.miny - 2, self.maxy + 3):
                if not self.grid.get((i, j)):
                    self.grid[(i, j)] = "."
        self.refresh_min_maxes()

        points = deque([(self.minx, self.miny)])
        while points:
            point = points.pop()
            self.grid[point] = "o"
            for neighbour in self.get_neighbours(point[0], point[1]):
                points.append(neighbour)

        num_outside = len([key for key in self.grid.keys() if self.grid[key] == "o"])

        return (self.maxx + 1 - self.minx) * (self.maxy + 1 - self.miny) - num_outside


def process_input(blob):
    blob = blob.replace("(#", "")
    blob = blob.replace(")", "")
    lines = []
    for line in blob.split("\n"):
        a, b, c = line.split(" ")
        lines.append((a, int(b), c))
    return lines


def do_part_1(lines):
    trench = Trench(["1"])
    trench.dig(lines)
    trench.refresh_min_maxes()
    return trench.get_v()


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None


# 42970 too high
# 38271 too low
# 39907 too low
