from utils.grid import Point


class Tetris:
    def __init__(self, instruction):
        self.points = {}

        self.instructions = instruction
        self.current_instruction = 0
        self.last_instruction = ""

        self.shapes = ["-", "+", "l", "i", "o"]
        self.current_shape = 0

        self.initialize()

    def initialize(self):
        self.points = {}
        self.points[Point(1, 0)] = "*"
        self.points[Point(2, 0)] = "*"
        self.points[Point(3, 0)] = "*"
        self.points[Point(4, 0)] = "*"
        self.points[Point(5, 0)] = "*"
        self.points[Point(6, 0)] = "*"
        self.points[Point(7, 0)] = "*"

    def create_new_shape(self):
        shape = self.shapes[self.current_shape]
        self.current_shape += 1
        self.current_shape = self.current_shape % (len(self.shapes))

        block = {}
        ref_y = self.highest_y + 4  # first y of the new shape

        if shape == "-":
            block[Point(3, ref_y)] = "-"
            block[Point(4, ref_y)] = "-"
            block[Point(5, ref_y)] = "-"
            block[Point(6, ref_y)] = "-"
        elif shape == "+":
            block[Point(4, ref_y)] = "+"
            block[Point(3, ref_y + 1)] = "+"
            block[Point(4, ref_y + 1)] = "+"
            block[Point(5, ref_y + 1)] = "+"
            block[Point(4, ref_y + 2)] = "+"
        elif shape == "l":
            block[Point(3, ref_y)] = "l"
            block[Point(4, ref_y)] = "l"
            block[Point(5, ref_y)] = "l"
            block[Point(5, ref_y + 1)] = "l"
            block[Point(5, ref_y + 2)] = "l"
        elif shape == "i":
            block[Point(3, ref_y)] = "i"
            block[Point(3, ref_y + 1)] = "i"
            block[Point(3, ref_y + 2)] = "i"
            block[Point(3, ref_y + 3)] = "i"
        elif shape == "o":
            block[Point(3, ref_y)] = "o"
            block[Point(4, ref_y)] = "o"
            block[Point(3, ref_y + 1)] = "o"
            block[Point(4, ref_y + 1)] = "o"
        return block

    def block_touches_ground(self, block):
        for b_point in block:
            for point in self.points:
                if b_point.x == point.x:
                    if b_point.y == point.y + 1:
                        return True
        return False

    def block_touches_left(self, block):
        if any([p.x == 1 for p in block]):
            return True
        for bp in block:
            for p in self.points:
                if bp.y == p.y and bp.x == p.x + 1:
                    return True
        return False

    def block_touches_right(self, block):
        if any([p.x == 7 for p in block]):
            return True
        for bp in block:
            for p in self.points:
                if bp.y == p.y and bp.x == p.x - 1:
                    return True
        return False

    @property
    def highest_y(self):
        return max([p.y for p in self.points])

    def run(self, num_block):
        for _ in range(num_block):
            block = self.create_new_shape()
            # self.print(block)
            v = 0
            while True:
                block = self.do_horizontal(block)
                # self.print(block)
                if self.block_touches_ground(block):
                    self.freeze(block)
                    # self.print(block)
                    break
                block = self.move_down(block)
                # self.print(block)
                z = 0

    def do_horizontal(self, block):
        instruction = self.instructions[self.current_instruction]
        self.last_instruction = instruction, self.current_instruction
        if instruction == ">":
            if not self.block_touches_right(block):
                block = self.move_right(block)
        elif instruction == "<":
            if not self.block_touches_left(block):
                block = self.move_left(block)
        self.current_instruction += 1
        self.current_instruction = self.current_instruction % len(self.instructions)
        return block

    def move_right(self, block):
        return {Point(p.x + 1, p.y): value for p, value in block.items()}

    def move_left(self, block):
        return {Point(p.x - 1, p.y): value for p, value in block.items()}

    def move_down(self, block):
        return {Point(p.x, p.y - 1): value for p, value in block.items()}

    def freeze(self, block):
        for p, value in block.items():
            self.points[p] = value

    def print(self, block):
        max_y = max([p.y for p in block])
        for y in range(max_y, -1, -1):
            line = ""
            for x in range(1, 8):
                p = self.points.get(Point(x, y))
                b = block.get(Point(x, y))
                if p:
                    line += p
                elif b:
                    line += b
                else:
                    line += "."
            print(line)
        print("\n")


def process_input(blob):
    return [c for c in blob]


def do_part_1(jets):
    tetris = Tetris(jets)
    tetris.run(2022)
    return tetris.highest_y


def do_part_2(processed_input):
    return "toto"
