from collections import defaultdict
import time

import matplotlib.pyplot as plt
import numpy

from utils.djikstra import djikstra


class Valley:
    def __init__(self, lines):
        self.grid = {}
        self.blizzards = defaultdict(list)
        self.b = set()  # blizzard posiitions
        self.initialize(lines)
        self.min_x, self.max_x, self.min_y, self.max_y = self.get_maxes()

        self.p1 = (1, 0)
        self.p2 = ((self.max_x - 1), self.max_y)

        self.destination = self.p2

        self.one_way = 0

        # Matplotlib stuff
        self.path = []
        self.done = False
        self.fig = None
        self.im = None
        self.ani = None

    def initialize(self, lines):
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == "#":
                    self.grid[(i, j)] = c
                elif c != ".":
                    self.blizzards[c].append((i, j))
                    self.b.add((i, j))

    def get_maxes(self):
        xes = [x for x, _ in self.grid.keys()]
        yes = [y for _, y in self.grid.keys()]
        return min(xes), max(xes), min(yes), max(yes)

    def print(self):
        for y in range(self.min_y, self.max_y + 1):
            line = ""
            for x in range(self.min_x, self.max_x + 1):
                if self.grid.get((x, y)):
                    line += "#"
                elif (x, y) in self.b:
                    line += "B"
                else:
                    line += "."
            print(line)
        print("\n")

    def edges_for_n_minutes(self, n):
        edges = []
        for t in range(n):
            new_edges = []
            # print(f"Minute {t}")
            # self.print()
            toto = 1
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    point = (x, y)
                    if self.grid.get(point) or (point in self.b):
                        continue

                    new_edges.append(
                        ((x, y, t - 1), (x, y, t), 1)
                    )  # stay same position

                    origins = [
                        (x, y - 1),
                        (x - 1, y),
                        (x + 1, y),
                        (x, y + 1),
                    ]
                    for x2, y2 in origins:
                        if (x, y) == self.destination:
                            new_edges.append(((x2, y2, t - 1), (x, y), 1))
                        else:
                            new_edges.append(((x2, y2, t - 1), (x, y, t), 1))
            edges.extend(new_edges)

            self.move_blizzards()
        return edges

    def move_blizzards(self):
        new_blizzards = defaultdict(list)
        new_positions = set()
        for direction, positions in self.blizzards.items():
            for x, y in positions:
                if direction == ">":
                    y2 = y
                    x2 = x + 1 if x < self.max_x - 1 else 1
                elif direction == "<":
                    y2 = y
                    x2 = x - 1 if x > 1 else self.max_x - 1
                elif direction == "^":
                    x2 = x
                    y2 = y - 1 if y > 1 else self.max_y - 1
                elif direction == "v":
                    x2 = x
                    y2 = y + 1 if y < self.max_y - 1 else 1
                else:
                    raise Exception
                new_blizzards[direction].append((x2, y2))
                new_positions.add((x2, y2))
        self.blizzards = new_blizzards
        self.b = new_positions

    def initialize_plot(self):
        plt.ion()
        self.fig = plt.figure(figsize=(18, 9))
        self.im = plt.imshow(self.get_grid((1, 0)), aspect="auto")
        plt.axis("off")
        plt.show()
        # time.sleep(0.05)

    def get_grid(self, point):
        plot_grid = numpy.zeros((self.max_y + 1, self.max_x + 1), dtype=int)

        x, y = point[:2]
        plot_grid[y][x] = 240  # elf

        for x, y in self.grid.keys():
            plot_grid[y][x] = 50  # walls
        for x, y in self.b:
            plot_grid[y][x] = 100  # tornados

        return plot_grid

    def animate(self):
        for point in self.path:
            self.move_blizzards()
            grid = self.get_grid(point)
            self.im.set_data(grid)
            self.fig.canvas.draw_idle()
            plt.pause(1)
        time.sleep(5)


def process_input(blob):
    lines = blob.split("\n")
    return Valley(lines), lines


def do_part_1(processed_input):
    valley, lines = processed_input

    max_minutes = 40 if len(lines) < 30 else 300

    edges = valley.edges_for_n_minutes(max_minutes)
    cost, path = djikstra(edges, (1, 0, 0), valley.destination)
    # print(cost)
    # print(path)

    # Visu
    # valley_p = Valley(lines)
    # valley_p.path = path
    # valley_p.initialize_plot()
    # valley_p.animate()
    return cost


def do_part_2(processed_input):
    _, lines = processed_input

    max_minutes = 40 if len(lines) < 30 else 300

    valley1 = Valley(lines)
    valley2 = Valley(lines)
    valley3 = Valley(lines)

    # Go
    valley1.destination = valley1.p2
    edges = valley1.edges_for_n_minutes(max_minutes)
    cost, path1 = djikstra(edges, valley1.p1 + (0,), valley1.destination)
    # print(cost)
    # print(path1)
    step1 = int(cost)

    # Back
    valley2.destination = valley2.p1
    _ = valley2.edges_for_n_minutes(step1)
    edges = valley2.edges_for_n_minutes(max_minutes)
    cost, path2 = djikstra(edges, valley2.p2 + (0,), valley2.destination)
    # print(cost)
    # print(path2)
    step2 = int(cost) + step1

    # Go
    valley3.destination = valley3.p2
    _ = valley3.edges_for_n_minutes(step2)
    edges = valley3.edges_for_n_minutes(max_minutes)
    cost, path3 = djikstra(edges, valley3.p1 + (0,), valley3.destination)
    # print(cost)
    # print(path3)

    # Visu
    # valley_p = Valley(lines)
    # valley_p.path = path1[1:] + path2[1:] + path3[1:]
    # valley_p.initialize_plot()
    # valley_p.animate()

    return step2 + cost
