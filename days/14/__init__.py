import os
from time import sleep


class Cave:
    def __init__(self, grid):
        self.grid = grid
        self.minx, self.maxx, self.miny, self.maxy = self.get_maxes()
        self.floor_y = None
        self.do_print = False

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
        for y in range(self.miny - 5, self.maxy + 6):
            line = f""
            for x in range(self.minx - 5, self.maxx + 10):
                line += self.get_xy(x, y, ".")
            print(line)
        print("\n")

    def get_xy(self, x, y, default=None):
        if y == self.floor_y:
            return "w"
        if y <= 0 and x != 500:
            return "v"
        else:
            return self.grid.get((x, y), default)

    def drop(self):
        x, y = 500, 0
        while True:
            if self.floor_y is None:
                if y == self.maxy:
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
            sleep(0.2)
        if x == 500 and y == 0:
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
                    grid[(x, y)] = "#"
    return Cave(grid), Cave(grid.copy())


def do_part_1(caves):
    cave, _ = caves
    num_drops = cave.fill()
    return num_drops


def do_part_2(caves):
    _, cave = caves
    cave.floor_y = cave.maxy + 2
    # cave.do_print = True
    num_drops = cave.fill()
    return num_drops + 1
