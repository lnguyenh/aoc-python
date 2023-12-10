import sys
from collections import defaultdict

from utils.djikstra import djikstra
from utils.grid import Grid


class Maze(Grid):
    def __init__(self, lines):
        self.animal = None
        super().__init__(lines)
        self.edges = []
        self.links = defaultdict(list)
        self.create_links()
        self.create_edges()
        self.start_loop = self.change_animal()
        self.print()
        x = 1

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
            elif c == "-":
                #
                self.edges.append((point, (x + 1, y), 1))
                self.edges.append(((x + 1, y), point, 1))
                #
                self.edges.append(((x - 1, y), point, 1))
                self.edges.append((point, (x - 1, y), 1))
            elif c == "L":
                #
                self.edges.append((point, (x + 1, y), 1))
                self.edges.append(((x + 1, y), point, 1))
                #
                self.edges.append(((x, y - 1), point, 1))
                self.edges.append((point, (x, y - 1), 1))
            elif c == "J":
                #
                self.edges.append((point, (x - 1, y), 1))
                self.edges.append(((x - 1, y), point, 1))
                #
                self.edges.append(((x, y - 1), point, 1))
                self.edges.append((point, (x, y - 1), 1))
            elif c == "7":
                #
                self.edges.append((point, (x - 1, y), 1))
                self.edges.append(((x - 1, y), point, 1))
                #
                self.edges.append(((x, y + 1), point, 1))
                self.edges.append((point, (x, y + 1), 1))
            elif c == "F":
                #
                self.edges.append((point, (x + 1, y), 1))
                self.edges.append(((x + 1, y), point, 1))
                #
                self.edges.append(((x, y + 1), point, 1))
                self.edges.append((point, (x, y + 1), 1))

    def get_distance_to_animal(self, point):
        distance, path = djikstra(self.edges, self.animal, point)
        return distance, path

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
                return (x + 1, y)
        if b and d:
            if b in ["|", "F", "7"] and d in ["J", "L", "|"]:
                self.grid[(x, y)] = "|"
                return (x, y + 1)

        if a and b:
            if a in ["-", "F", "L"] and b in ["|", "F", "7"]:
                self.grid[(x, y)] = "J"
                return (x, y - 1)
        if a and d:
            if a in ["-", "F", "L"] and d in ["|", "J", "L"]:
                self.grid[(x, y)] = "7"
                return (x, y + 1)

        if d and c:
            if d in ["L", "J", "|"] and c in ["-", "J", "7"]:
                self.grid[(x, y)] = "F"
                return (x + 1, y)
        if b and c:
            if b in ["|", "7", "F"] and c in ["-", "J", "7"]:
                self.grid[(x, y)] = "L"
                return (x, y - 1)
        raise Exception

    def expand_grid(self):
        new_points_in_grid = {}

        # self.change_animal()

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

        grid = {}
        for key, value in new_points_in_grid.items():
            x, y = key
            new_key = (int(x * 2), int(y * 2))
            grid[new_key] = value
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

    def expand_zone(self, zone):
        points_to_add = set()
        for point in zone:
            x, y = point
            a = (x - 1, y)
            b = (x, y - 1)
            c = (x + 1, y)
            d = (x, y + 1)
            for p in [a, b, c, d]:
                if p not in zone:
                    if p not in self.grid:
                        return 0
                    if self.grid.get(p) in [".", "x"]:
                        points_to_add.add(p)

        if points_to_add:
            return self.expand_zone(zone.union(points_to_add))
        return 1

    def expand_outside_zone(self, zone):
        points_to_add = set()
        for point in zone:
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
            return self.expand_outside_zone(zone.union(points_to_add))
        else:
            return zone

    def simplify(self):
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
            points_to_simplify = self.expand_outside_zone({edge_dots[0]})
            for p in points_to_simplify:
                self.grid[p] = " "
            # self.print()
            x = 1

        self.print()

    def do_part_2(self):
        dots = [p for p in self.points if self.grid[p] == "."]
        # return sum([self.expand_zone({dot}) for dot in dots])
        return len(dots)


def process_input(blob):
    lines = blob.split("\n")
    maze = Maze(lines)
    return maze


def do_part_1(maze):
    length, _ = maze.trace_loop()
    return int(round(length / 2))


def do_part_2(maze):
    # return "toto"
    print("BEFORE CLEAN")
    maze.print()
    maze.clean_grid()
    print("BEFORE EXPAND")
    maze.print()
    maze.expand_grid()
    print("AFTER EXPAND")
    maze.print()
    maze.simplify()
    print("AFTER SIMPLIFY")
    # maze.print()
    return maze.do_part_2()


def do_visualization(processed_input):
    return None
