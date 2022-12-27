from utils.grid import Grid
from year2019.intcode import IntCode


class Hull(Grid):
    SKIP = (".",)
    PRINT = {
        "w": "*",
        "b": " ",
    }

    def __init__(self, lines):
        super().__init__(lines)
        self.position = (0, 0)
        self.direction = 0  # 0 up, 1 right, 2 down, 3 left

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def turn_left(self):
        self.direction = (self.direction - 1) % 4

    def move_forward(self):
        x, y = self.position  # y pointing down
        candidates = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        self.position = candidates[self.direction]

    def paint_white(self):
        self.grid[self.position] = "w"

    def paint_black(self):
        self.grid[self.position] = "b"

    def get_color(self):
        return 1 if self.grid.get(self.position) == "w" else 0

    def count_painted(self):
        return len(self.grid.keys())


def process_input(blob):
    return [int(n) for n in blob.split(",")]


def do_part_1(program):
    hull = Hull([])
    intcode = IntCode(program, seed=[0], silent=True, seed_only=True)
    while intcode.is_not_done:
        intcode.resume()
        (color, turn) = intcode.read_all()
        if color == 0:
            hull.paint_black()
        else:
            hull.paint_white()
        if turn == 0:
            hull.turn_left()
        else:
            hull.turn_right()
        hull.move_forward()
        intcode.add_to_seed(hull.get_color())

    return hull.count_painted()


def do_part_2(program):
    hull = Hull([])
    intcode = IntCode(program, seed=[1], silent=True, seed_only=True)
    while intcode.is_not_done:
        intcode.resume()
        (color, turn) = intcode.read_all()
        if color == 0:
            hull.paint_black()
        else:
            hull.paint_white()
        if turn == 0:
            hull.turn_left()
        else:
            hull.turn_right()
        hull.move_forward()
        intcode.add_to_seed(hull.get_color())

    hull.print()

    return "toto"


def do_visualization(processed_input):
    return None
