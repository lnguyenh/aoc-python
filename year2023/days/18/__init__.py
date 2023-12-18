from collections import deque
from dataclasses import dataclass

from utils.grid import Grid


DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "D": (0, 1),
    "U": (0, -1),
}

TRANSLATION = {"0": "R", "1": "D", "2": "L", "3": "U"}


@dataclass
class Block:
    value: str
    xes: tuple[int]
    yes: tuple[int]

    @property
    def area(self):
        return (self.xes[1] - self.xes[0] + 1) * (self.yes[1] - self.yes[0] + 1)


def set_blocks_value(start_x, stop_x, start_y, stop_y, grid, c):
    # Part 2 helper
    grid_ids = []
    for (i, j), block in grid.items():
        if start_x in block.xes and stop_x in block.xes:
            if start_y <= block.yes[1] <= stop_y or stop_y <= block.yes[1] <= start_y:
                grid_ids.append((i, j))
        if start_y in block.yes and stop_y in block.yes:
            if start_x <= block.xes[1] <= stop_x or stop_x <= block.xes[1] <= start_x:
                grid_ids.append((i, j))
    for (i, j) in grid_ids:
        grid[(i, j)].value = c


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

        outside_keys = [key for key in self.grid.keys() if self.grid[key] == "o"]
        num_outside = len(outside_keys)
        insides_keys = [key for key in self.grid.keys() if self.grid[key] != "o"]

        return (self.maxx + 1 - self.minx) * (
            self.maxy + 1 - self.miny
        ) - num_outside, insides_keys


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
    return trench.get_v()[0]


def do_part_2(lines):
    new_lines = []

    for line in lines:
        _, _, hexa = line
        d = hexa[-1]
        n = int(hexa[:-1], 16)
        new_lines.append((TRANSLATION[d], n, "x"))

    x_bounds = {0}
    y_bounds = {0}
    x = 0
    y = 0
    for d, n, _ in new_lines:
        if d == "U":
            y -= n
        elif d == "D":
            y += n
        elif d == "R":
            x += n
        elif d == "L":
            x -= n
        x_bounds.add(x)
        y_bounds.add(y)
    x_bounds.update([min(x_bounds) - 3, max(x_bounds) + 3])
    y_bounds.update([min(y_bounds) - 3, max(y_bounds) + 3])
    x_bounds = sorted(list(x_bounds))
    y_bounds = sorted(list(y_bounds))

    last_x = None
    x_ints = []
    for x in x_bounds:
        if last_x is not None:
            x_ints.append((last_x + 1, x - 1))
            x_ints.append((x, x))
        last_x = x

    last_y = None
    y_ints = []
    for y in y_bounds:
        if last_y is not None:
            y_ints.append((last_y + 1, y - 1))
            y_ints.append((y, y))
        last_y = y

    grid = {}
    blocks = {}
    for i, x_int in enumerate(x_ints):
        for j, y_int in enumerate(y_ints):
            grid[(i, j)] = Block(".", x_int, y_int)
            blocks[(x_int, y_int)] = (i, j)

    x, y = (0, 0)
    for d, n, _ in new_lines:
        stop_x = x + n * DIRECTIONS[d][0]
        stop_y = y + n * DIRECTIONS[d][1]
        set_blocks_value(x, stop_x, y, stop_y, grid, "#")
        x = stop_x
        y = stop_y

    trench = Trench(["1"])
    abstract_grid = {point: "#" for point, block in grid.items() if block.value == "#"}
    trench.grid = abstract_grid
    trench.refresh_min_maxes()
    inside_block_ids = trench.get_v()[1]
    return sum([grid[block_id].area for block_id in inside_block_ids])


def do_visualization(processed_input):
    return None
