from collections import defaultdict

from utils.grid import Grid


class Platform(Grid):
    SKIP = (".",)

    def __init__(self, lines):
        super().__init__(lines)
        self.states = defaultdict(list)

    def tilt_north(self):
        moved = True
        while moved:
            moved = False
            for j in range(self.maxy + 1):
                for i in range(self.maxx + 1):
                    c = self.grid.get((i, j))
                    if c == "O":
                        tx, ty = i, j - 1
                        if ty >= 0 and (tx, ty) not in self.grid:
                            self.grid[(tx, ty)] = c
                            self.grid.pop((i, j))
                            moved = True

    def tilt_south(self):
        moved = True
        while moved:
            moved = False
            for j in range(self.maxy, self.miny - 1, -1):
                for i in range(self.maxx + 1):
                    c = self.grid.get((i, j))
                    if c == "O":
                        tx, ty = i, j + 1
                        if ty <= self.maxy and (tx, ty) not in self.grid:
                            self.grid[(tx, ty)] = c
                            self.grid.pop((i, j))
                            moved = True

    def tilt_west(self):
        moved = True
        while moved:
            moved = False
            for i in range(self.maxx + 1):
                for j in range(self.maxy + 1):
                    c = self.grid.get((i, j))
                    if c == "O":
                        tx, ty = i - 1, j
                        if tx >= 0 and (tx, ty) not in self.grid:
                            self.grid[(tx, ty)] = c
                            self.grid.pop((i, j))
                            moved = True

    def tilt_east(self):
        moved = True
        while moved:
            moved = False
            for i in range(self.maxx + 1, -1, -1):
                for j in range(self.maxy + 1):
                    c = self.grid.get((i, j))
                    if c == "O":
                        tx, ty = i + 1, j
                        if tx <= self.maxx and (tx, ty) not in self.grid:
                            self.grid[(tx, ty)] = c
                            self.grid.pop((i, j))
                            moved = True

    def do_one_cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def save_state(self, i):
        state = tuple(self.grid.keys())
        # print(state)
        self.states[state].append(i)
        return self.states[state]

    def get_weight(self):
        weights = []
        for (i, j), c in self.grid.items():
            if c == "O":
                weights.append(self.maxy + 1 - j)
        return sum(weights)


def process_input(blob):
    return Platform(blob.split("\n"))


def do_part_1(platform):
    platform.tilt_north()
    return platform.get_weight()


def do_part_2(platform):
    i = 0
    while True:
        platform.do_one_cycle()
        x = platform.save_state(i)
        i += 1
        if len(x) == 2:
            cycle_length = x[1] - x[0]
            num_cycles_left = (999999999 - x[0]) % cycle_length
            for _ in range(num_cycles_left):
                platform.do_one_cycle()
            return platform.get_weight()


def do_visualization(processed_input):
    return None
