from utils.grid import Grid


class Map(Grid):
    SKIP = (".",)

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
            if n == "@":
                result.append(n)
        return result

    def can_be_accessed(self, point):
        return len(self.real_neighbours(point)) < 4


def process_input(blob):
    lines = blob.split("\n")
    return Map(lines), Map(lines)


def do_part_1(processed_input):
    mappy = processed_input[0]
    count = 0
    for point in mappy.points:
        if mappy.can_be_accessed(point):
            count += 1
    return count


def do_part_2(processed_input):
    mappy = processed_input[1]
    count = 0
    while True:
        done_this_turn = 0
        for point in mappy.points:
            x, y = point
            if mappy.grid[(x, y)] != "x" and mappy.can_be_accessed(point):
                mappy.grid[(x, y)] = "x"
                count += 1
                done_this_turn += 1
        if done_this_turn == 0:
            break
    return count


def do_visualization(processed_input):
    return None
