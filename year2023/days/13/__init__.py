from utils.grid import Grid


class Field(Grid):
    SKIP = (".",)

    def __init__(self, lines):
        super().__init__(lines)

    def find_vertical(self):
        for i in range(self.maxx):
            i1 = i
            i2 = i + 1
            if self.count_vertical_diffs(i1, i2) == 0:
                # i is candidate for reflection
                i1 -= 1
                i2 += 1
                is_ok = True
                while self.minx <= i1 and i2 <= self.maxx:
                    if self.count_vertical_diffs(i1, i2) != 0:
                        is_ok = False
                        break
                    i1 -= 1
                    i2 += 1
                if is_ok:
                    return i + 1
        return 0

    def find_horizontal(self):
        for j in range(self.maxy):
            j1 = j
            j2 = j + 1
            if self.count_horizontal_diffs(j1, j2) == 0:
                # j is candidate for reflection
                j1 -= 1
                j2 += 1
                is_ok = True
                while 0 <= j1 and j2 <= self.maxy:
                    if self.count_horizontal_diffs(j1, j2) != 0:
                        is_ok = False
                        break
                    j1 -= 1
                    j2 += 1
                if is_ok:
                    return (j + 1) * 100
        return 0

    def count_vertical_diffs(self, i1, i2):
        return sum(
            [
                1
                for j in range(self.maxy + 1)
                if self.grid.get((i1, j)) != self.grid.get((i2, j))
            ]
        )

    def count_horizontal_diffs(self, j1, j2):
        return sum(
            [
                1
                for i in range(self.maxx + 1)
                if self.grid.get((i, j1)) != self.grid.get((i, j2))
            ]
        )

    def find_vertical_2(self):
        for i in range(self.maxx):
            i1 = i
            i2 = i + 1
            if all(
                [
                    self.grid.get((i1, j)) == self.grid.get((i2, j))
                    for j in range(self.maxy + 1)
                ]
            ):
                # i is candidate for reflection
                i1 -= 1
                i2 += 1
                is_ok = True
                while self.minx <= i1 and i2 <= self.maxx:
                    if not all(
                        [
                            self.grid.get((i1, j)) == self.grid.get((i2, j))
                            for j in range(self.maxy + 1)
                        ]
                    ):
                        is_ok = False
                        break
                    i1 -= 1
                    i2 += 1
                if is_ok:
                    return i + 1
        return 0

    def find_horizontal_2(self):
        for j in range(self.maxy):
            j1 = j
            j2 = j + 1
            if all(
                [
                    self.grid.get((i, j1)) == self.grid.get((i, j2))
                    for i in range(self.maxx + 1)
                ]
            ):
                # j is candidate for reflection
                j1 -= 1
                j2 += 1
                is_ok = True
                while 0 <= j1 and j2 <= self.maxy:
                    if not all(
                        [
                            self.grid.get((i, j1)) == self.grid.get((i, j2))
                            for i in range(self.maxx + 1)
                        ]
                    ):
                        is_ok = False
                        break
                    j1 -= 1
                    j2 += 1
                if is_ok:
                    return (j + 1) * 100
        return 0


def process_input(blob):
    grids = blob.split("\n\n")
    return [Field(grid.split("\n")) for grid in grids]


def do_part_1(processed_input):
    fields = processed_input
    results = [field.find_horizontal() + field.find_vertical() for field in fields]
    return sum(results)


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
