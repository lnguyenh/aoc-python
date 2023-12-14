from utils.grid import Grid


class Platform(Grid):
    SKIP = (".",)

    def __init__(self, lines):
        super().__init__(lines)

    def tilt_north(self):
        moved = True
        while moved:
            moved = False
            for j in range(self.maxy + 1):
                for i in range(self.maxx + 1):
                    c = self.grid.get((i, j))
                    if c == "O":
                        tx, ty = i, j - 1
                        if j - 1 >= 0 and (tx, ty) not in self.grid:
                            self.grid[(tx, ty)] = c
                            self.grid.pop((i, j))
                            moved = True

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


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
