from utils.grid import Grid

ROLL = 150
REMOVED_ROLL = 100
EMPTY = 1


class Map(Grid):
    SKIP = (".",)
    TRANSLATE = {"@": ROLL, ".": EMPTY}
    PLOT_BOX = (136, 136)
    CMAP = "bone"
    DELAY_AFTER_REFRESH = 0.001
    FIGSIZE = (10, 10)

    def __init__(self, lines):
        super().__init__(lines)

    def neighbours(self, point):
        return [
            self.point_up(point),
            self.point_down(point),
            self.point_left(point),
            self.point_right(point),
            self.point_up_left(point),
            self.point_up_right(point),
            self.point_down_left(point),
            self.point_down_right(point),
        ]

    def real_neighbours(self, point):
        result = []
        for n in self.neighbours(point):
            if n == ROLL:
                result.append(n)
        return result

    def can_be_accessed(self, point):
        return len(self.real_neighbours(point)) < 4


def process_input(blob):
    return blob.split("\n")


def do_part_1(processed_input):
    mappy = Map(processed_input)
    count = 0
    for point in mappy.points:
        if mappy.can_be_accessed(point):
            count += 1
    return count


def do_part_2(processed_input):
    mappy = Map(processed_input)
    count = 0
    while True:
        done_this_turn = 0
        for point in mappy.points:
            x, y = point
            if mappy.grid[(x, y)] != REMOVED_ROLL and mappy.can_be_accessed(point):
                mappy.grid[(x, y)] = REMOVED_ROLL
                count += 1
                done_this_turn += 1
        if done_this_turn == 0:
            break
    return count


def do_visualization(processed_input):
    mappy = Map(processed_input)
    mappy.initialize_plot()
    count = 0
    while True:
        done_this_turn = 0
        for point in mappy.points:
            x, y = point
            if mappy.grid[(x, y)] != REMOVED_ROLL and mappy.can_be_accessed(point):
                mappy.grid[(x, y)] = REMOVED_ROLL
                mappy.refresh_plot()
                count += 1
                done_this_turn += 1
        if done_this_turn == 0:
            break
    return count
