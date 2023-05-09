import matplotlib.pyplot as plt
import numpy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x={self.x}, y={self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(tuple((self.x, self.y)))


class Grid:

    TRANSLATE = {}  # characters to save in the grid as some other value
    SKIP = tuple()  # tuple with characters to not save in the grid
    PRINT = {}  # special translations when printing (see 2019 day 11 for example)

    PLOT_BOX = (300, 200)  # visualization box (Y, X)
    PLOT = {}  # special translations when animating (see 2019 day 11 for example)
    X_OFFSET = 0
    Y_OFFSET = 0
    CMAP = None  # "bones", ...
    FIGSIZE = None  # ex: (18, 9) used to change size/ratio

    def __init__(self, lines, *args, **kwargs):
        self.grid = {}
        self.populate_grid(lines)

        # Matplotlib stuff
        self.path = []
        self.done = False
        self.fig = None
        self.im = None
        self.ax = None

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

    def get_plot_grid(self):
        plot_grid = numpy.zeros(self.PLOT_BOX, dtype=int)

        for key, c in self.grid.items():
            x, y = key
            plot_grid[y + self.Y_OFFSET][x + self.X_OFFSET] = self.PLOT.get(c, c)

        return plot_grid

    def add_to_plot(self, plot_grid):
        # - Override to add special stuff to the grid
        # - Example of text overlay in 2019 day 13
        return None

    def initialize_plot(self):
        plt.ion()
        self.fig = plt.figure(figsize=self.FIGSIZE)
        self.ax = self.fig.add_subplot()
        self.im = plt.imshow(
            self.get_plot_grid(), aspect="auto", cmap=self.CMAP, vmin=0, vmax=500
        )
        plt.axis("off")
        plt.show()

    def refresh_plot(self):
        grid = self.get_plot_grid()
        self.add_to_plot(grid)
        self.im.set_data(grid)
        self.fig.canvas.draw_idle()
        plt.pause(0.01)

    def print_box_size(self):
        # Can be used to help finding good setting for visualization
        x_min, x_max, y_min, y_max = self.get_min_maxes()
        print(f"y_min: {y_min}, y_max: {y_max}, total_y = {y_max - y_min}")
        print(f"x_min: {x_min}, x_max: {x_max}, total_x = {x_max - x_min}")
