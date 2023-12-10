import sys
from collections import defaultdict
from time import sleep

from utils.grid import Grid


class Maze(Grid):
    PLOT = {
        "F": 5,
        "J": 5,
        "|": 5,
        "7": 5,
        "-": 5,
        "L": 5,
        ".": 100,
        "x": 300,  # Used when expanding the grid. Means the same than dots but is "virtual"
        " ": 500,  # Used when removing all non relevant points outside the loop
        "H": 1500,  # Used for flashing animation
    }
    PLOT_BOX = (280, 280)
    CMAP = "bone"
    FIGSIZE = (10, 10)

    def __init__(self, lines, visu=False):
        self.animal = None
        super().__init__(lines)
        self.links = defaultdict(list)
        self.create_links()
        self.start_loop = self.change_animal()
        self.visu = visu  # visualization flag
        if visu:
            self.initialize_plot()

    def populate_grid(self, lines):
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                self.set_grid_value(i, j, c)
                if c == "S":
                    self.animal = (i, j)

    def create_links(self):
        for x, y in self.points:
            point = (x, y)
            c = self.grid[(x, y)]
            if c == "|":
                self.links[point].append((x, y + 1))
                self.links[point].append((x, y - 1))
            elif c == "-":
                self.links[point].append((x + 1, y))
                self.links[point].append((x - 1, y))
            elif c == "L":
                self.links[point].append((x + 1, y))
                self.links[point].append((x, y - 1))
            elif c == "J":
                self.links[point].append((x - 1, y))
                self.links[point].append((x, y - 1))
            elif c == "7":
                self.links[point].append((x - 1, y))
                self.links[point].append((x, y + 1))
            elif c == "F":
                self.links[point].append((x + 1, y))
                self.links[point].append((x, y + 1))

    def get_point_to(self, point_from, point_current):
        z = [point for point in self.links[point_current] if point != point_from]
        return z[0]

    def trace_loop(self):

        point_from = self.animal
        point_current = self.start_loop
        loop = [point_from, point_current]
        while True:
            point_to = self.get_point_to(point_from, point_current)
            loop.append(point_to)
            if point_to == self.animal:
                break
            point_from = point_current
            point_current = point_to

        return len(loop), loop

    def clean_grid(self):
        _, loop = self.trace_loop()
        for point in self.points:
            if point not in loop:
                self.grid[point] = "."

    def change_animal(self):
        x, y = self.animal
        a = self.grid.get((x - 1, y))
        b = self.grid.get((x, y - 1))
        c = self.grid.get((x + 1, y))
        d = self.grid.get((x, y + 1))

        if a and c:
            if a in ["-", "L", "F"] and c in ["-", "7", "J"]:
                self.grid[(x, y)] = "-"
                return x + 1, y
        if b and d:
            if b in ["|", "F", "7"] and d in ["J", "L", "|"]:
                self.grid[(x, y)] = "|"
                return x, y + 1
        if a and b:
            if a in ["-", "F", "L"] and b in ["|", "F", "7"]:
                self.grid[(x, y)] = "J"
                return x, y - 1
        if a and d:
            if a in ["-", "F", "L"] and d in ["|", "J", "L"]:
                self.grid[(x, y)] = "7"
                return x, y + 1
        if d and c:
            if d in ["L", "J", "|"] and c in ["-", "J", "7"]:
                self.grid[(x, y)] = "F"
                return x + 1, y
        if b and c:
            if b in ["|", "7", "F"] and c in ["-", "J", "7"]:
                self.grid[(x, y)] = "L"
                return x, y - 1
        raise Exception

    def expand_grid(self):
        new_points_in_grid = {}
        for x, y in self.points:
            current = self.grid[(x, y)]
            a = (x - 1, y)
            b = (x, y - 1)
            c = (x + 1, y)
            d = (x, y + 1)

            if self.grid.get(a):
                if self.grid[a] in ["-", "L", "F"] and current in ["-", "7", "J"]:
                    new_points_in_grid[(x - 0.5, y)] = "-"
                else:
                    new_points_in_grid[(x - 0.5, y)] = "x"

            if self.grid.get(c):
                if current in ["-", "L", "F"] and self.grid[c] in ["-", "7", "J"]:
                    new_points_in_grid[(x + 0.5, y)] = "-"
                else:
                    new_points_in_grid[(x + 0.5, y)] = "x"

            if self.grid.get(b):
                if self.grid[b] in ["|", "F", "7"] and current in ["J", "L", "|"]:
                    new_points_in_grid[(x, y - 0.5)] = "|"
                else:
                    new_points_in_grid[(x, y - 0.5)] = "x"

            if self.grid.get(d):
                if current in ["|", "F", "7"] and self.grid[d] in ["J", "L", "|"]:
                    new_points_in_grid[(x, y + 0.5)] = "|"
                else:
                    new_points_in_grid[(x, y + 0.5)] = "x"

        self.grid.update(new_points_in_grid)
        grid = {}
        for key, value in self.grid.items():
            x, y = key
            new_key = (int(x * 2), int(y * 2))
            grid[new_key] = value

        self.grid = grid
        x_min, x_max, y_min, y_max = self.get_min_maxes()
        for j in range(y_min, y_max + 1):
            for i in range(x_min, x_max + 1):
                if not grid.get((i, j)):
                    grid[(i, j)] = "x"

    def expand_outside_zone(self, zone, new_points):
        points_to_add = set()
        for point in new_points:
            x, y = point
            a = (x - 1, y)
            b = (x, y - 1)
            c = (x + 1, y)
            d = (x, y + 1)
            for p in [a, b, c, d]:
                if p not in zone:
                    if self.grid.get(p) in [".", "x"]:
                        points_to_add.add(p)

        if points_to_add:
            return self.expand_outside_zone(zone.union(points_to_add), points_to_add)
        else:
            return zone

    def simplify(self):
        # Remove all dots that our outside the loop.
        # Done by expanding all the dots touching the border of the image
        sys.setrecursionlimit(10000)
        x_min, x_max, y_min, y_max = self.get_min_maxes()

        while True:
            edge_dots = [
                (x, y)
                for (x, y) in self.points
                if self.grid[(x, y)] == "."
                and (x in [x_min, x_max] or y in [y_min, y_max])
            ]
            if not edge_dots:
                break
            points_to_simplify = self.expand_outside_zone(
                {edge_dots[0]}, {edge_dots[0]}
            )
            for i, p in enumerate(points_to_simplify):
                if self.visu and i % 125 == 0:
                    self.refresh_plot()
                self.grid[p] = " "  # all points outside the loop

    def do_part_2(self):
        self.clean_grid()
        self.expand_grid()
        if self.visu:
            self.refresh_plot()
            sleep(5)
        self.simplify()
        return len([p for p in self.points if self.grid[p] == "."])

    def highlight_dots(self):
        # Flashing animation when doing visualization
        points = [p for p in self.points if self.grid[p] == "."]
        for i in range(200):
            if i % 2:
                value = 1500
            else:
                value = 0
            for point in points:
                self.grid[point] = value

            if self.visu:
                self.refresh_plot()


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    maze = Maze(lines)
    length, _ = maze.trace_loop()
    return int(round(length / 2))


def do_part_2(lines):
    maze = Maze(lines)
    return maze.do_part_2()


def do_visualization(lines):
    maze = Maze(lines, visu=True)
    maze.do_part_2()
    maze.highlight_dots()
