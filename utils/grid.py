class Grid:

    TRANSLATE = {}  # characters to save in the grid as some other value
    SKIP = tuple()  # tuple with characters to not save in the grid
    PRINT = {}  # special translations when printing (see 2019 day 11 for example)

    def __init__(self, lines, *args, **kwargs):
        self.grid = {}
        self.populate_grid(lines)

    @property
    def points(self):
        return self.grid.keys()

    def populate_grid(self, lines):
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                self.set_grid_value(i, j, c)

    def set_grid_value(self, i, j, c):
        if c not in self.SKIP:
            value = self.TRANSLATE.get(c, c)  # find a translation or default to c
            self.grid[(i, j)] = value

    def get_min_maxes(self):
        xes = [x for x, _ in self.grid.keys()]
        yes = [y for _, y in self.grid.keys()]
        return min(xes), max(xes), min(yes), max(yes)

    def print(self):
        x_min, x_max, y_min, y_max = self.get_min_maxes()
        for j in range(y_min, y_max + 1):
            line = ""
            for i in range(x_min, x_max + 1):
                c = self.grid.get((i, j), " ")
                c = self.PRINT.get(c, c)
                line += c
            print(line)
        print("\n")
