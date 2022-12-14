import os
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
import numpy as np


class Cave:
    def __init__(self, grid):
        self.grid = grid
        self.minx, self.maxx, self.miny, self.maxy = self.get_maxes()
        self.floor_y = None
        self.do_print = False
        self.tmp_grid = {}

        # Matplotlib stuff
        self.done = False
        self.fig = None
        self.im = None
        self.ani = None

    def initialize_plot(self):
        self.fig = plt.figure()
        self.im = plt.imshow(self.get_plot_grid(), animated=True, aspect="auto")
        plt.axis("off")

    def get_plot_grid(self):
        plot_grid = numpy.zeros((200, 700), dtype=int)
        for xy in self.grid.keys():
            x, y = xy
            char = self.get_xy(x, y)
            val = 0
            if char == "*":
                val = 255
            elif char == "o":
                val = 100
            plot_grid[y][x] = val
        for xy in self.tmp_grid.keys():
            x, y = xy
            plot_grid[y][x] = 200
        for x in range(700):
            for y in range(self.maxy + 2, 200):
                plot_grid[y][x] = 300
        plot_grid = plot_grid[0:180, 310:700]
        return plot_grid

    def update(self, i):
        if self.done:
            return (self.im,)
        self.drop()
        self.im.set_array(self.get_plot_grid())
        return (self.im,)

    def animate(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1, blit=True)
        plt.show()
        return self.ani

    def get_maxes(self):
        minx = maxx = miny = maxy = None
        for xy in self.grid.keys():
            x, y = xy
            if minx is None or x < minx:
                minx = x
            if miny is None or y < miny:
                miny = y
            if maxx is None or x > maxx:
                maxx = x
            if maxy is None or y > maxy:
                maxy = y
        return minx, maxx, miny, maxy

    def print(self):
        os.system("clear")
        # for y in range(self.miny - 5, self.maxy + 6):
        for y in range(-1, 175):
            line = f""
            # for x in range(self.minx - 5, self.maxx + 10):
            for x in range(300, 700):
                line += self.get_xy(x, y, " ")
            print(line)

    def get_xy(self, x, y, default=None):
        if y == self.floor_y:
            return "w"
        if y <= 0 and x != 500:
            return "v"
        else:
            return self.grid.get((x, y), default)

    def drop(self):
        x, y = 500, 0
        self.tmp_grid = {}
        while True:
            # Used for the visualisation
            self.tmp_grid[(x, y)] = "c"

            if self.floor_y is None:
                if y == self.maxy:
                    self.done = True
                    return -1

            left = self.get_xy(x - 1, y + 1)
            center = self.get_xy(x, y + 1)
            right = self.get_xy(x + 1, y + 1)

            if not center:
                x, y = x, y + 1
            elif not left:
                x, y = x - 1, y + 1
            elif not right:
                x, y = x + 1, y + 1
            else:
                break
        self.grid[(x, y)] = "o"

        if self.do_print:
            self.print()
            sleep(0.005)

        if x == 500 and y == 0:
            self.done = True
            return -1
        return 0

    def fill(self):
        num_drops = 0
        while True:
            result = self.drop()
            num_drops += 1
            if result == -1:
                break
        return num_drops - 1


def process_input(blob):
    grid = {}
    lines = blob.split("\n")
    for line in lines:
        points = []
        for xy in line.split(" -> "):
            x, y = xy.split(",")
            x = int(x)
            y = int(y)
            points.append((x, y))
        for i in range(len(points) - 1):
            from_x, from_y = points[i]
            to_x, to_y = points[i + 1]
            dir_x = (
                int((to_x - from_x) / abs(to_x - from_x)) if abs(to_x - from_x) else 1
            )
            dir_y = (
                int((to_y - from_y) / abs(to_y - from_y)) if abs(to_y - from_y) else 1
            )
            for x in range(from_x, to_x + dir_x, dir_x):
                for y in range(from_y, to_y + dir_y, dir_y):
                    grid[(x, y)] = "*"
    return Cave(grid), Cave(grid.copy())


def do_part_1(caves):
    cave, _ = caves
    num_drops = cave.fill()
    return num_drops


def do_part_2(caves):
    _, cave = caves
    cave.floor_y = cave.maxy + 2

    # Uncomment to show the matplotlib animation
    cave.initialize_plot()
    cave.animate()

    num_drops = cave.fill()
    return num_drops + 1
