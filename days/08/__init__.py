class Forest:
    def __init__(self, lines):
        self.grid = {}

        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                self.grid[(j, i)] = int(c)

        # Convenience shortcuts
        self.points = self.grid.keys()
        self.max_x = max([key[0] for key in self.points])
        self.max_y = max([key[1] for key in self.points])
        self.x_bound = self.max_x + 1
        self.y_bound = self.max_y + 1

        self.visible = {key: False for key in self.points}
        self.populate_visibility()

        self.scenic = {}
        self.populate_scenic()

    def get_heights_from_directions(self):
        up = {}
        left = {}
        right = {}
        down = {}

        for x in range(1, self.x_bound):
            top = 0
            for y in range(0, self.y_bound):
                if self.grid[(x, y)] > top:
                    top = self.grid[(x, y)]
                up[(x, y + 1)] = top
        for y in range(1, self.y_bound):
            top = 0
            for x in range(0, self.x_bound):
                if self.grid[(x, y)] > top:
                    top = self.grid[(x, y)]
                left[(x + 1, y)] = top
        for x in range(1, self.x_bound):
            top = 0
            for y in range(self.max_y, 0, -1):
                if self.grid[(x, y)] > top:
                    top = self.grid[(x, y)]
                down[(x, y - 1)] = top
        for y in range(1, self.y_bound):
            top = 0
            for x in range(self.max_x, 0, -1):
                if self.grid[(x, y)] > top:
                    top = self.grid[(x, y)]
                right[(x - 1, y)] = top
        return up, down, left, right

    def populate_visibility(self):
        up, down, left, right = self.get_heights_from_directions()
        for point in self.points:
            if point[0] in [0, self.max_x] or point[1] in [0, self.max_y]:
                self.visible[point] = True
                continue
            height = self.grid[point]
            self.visible[point] = any(
                [
                    height > up[point],
                    height > down[point],
                    height > left[point],
                    height > right[point],
                ]
            )

    def populate_scenic(self):
        for x, y in self.points:
            if x in [0, self.max_x] or y in [0, self.max_y]:
                self.scenic[(x, y)] = 0
                continue
            height = self.grid[(x, y)]
            xr_scenic = 0
            xl_scenic = 0
            yu_scenic = 0
            yd_scenic = 0
            for xr in range(x + 1, self.x_bound):
                xr_scenic += 1
                if self.grid[(xr, y)] >= height:
                    break
            for xl in range(x - 1, -1, -1):
                xl_scenic += 1
                if self.grid[(xl, y)] >= height:
                    break
            for yd in range(y + 1, self.y_bound):
                yd_scenic += 1
                if self.grid[(x, yd)] >= height:
                    break
            for yu in range(y - 1, -1, -1):
                yu_scenic += 1
                if self.grid[(x, yu)] >= height:
                    break
            self.scenic[(x, y)] = xr_scenic * xl_scenic * yd_scenic * yu_scenic

    def count_visible(self):
        return sum([self.visible[point] for point in self.points])

    def max_scenic(self):
        return max([self.scenic[point] for point in self.points])


def process_input(blob):
    return Forest(blob.split("\n"))


def do_part_1(forest):
    return forest.count_visible()


def do_part_2(forest):
    return forest.max_scenic()
