class Rope:
    def __init__(self, instructions):
        self.instructions = instructions
        self.h = (0, 0)
        self.t = (0, 0)
        self.visited = {(0, 0)}

    def move(self, instruction):
        direction, steps = instruction
        for _ in range(steps):
            x, y = self.h
            if direction == "R":
                self.h = (x + 1, y)
            elif direction == "L":
                self.h = (x - 1, y)
            elif direction == "U":
                self.h = (x, y + 1)
            elif direction == "D":
                self.h = (x, y - 1)
            self.move_tail(x, y)

    def move_tail(self, h_origin_x, h_origin_y):
        x_diff = abs(self.h[0] - self.t[0])
        y_diff = abs(self.h[1] - self.t[1])
        if x_diff > 1 or y_diff > 1:
            self.t = [h_origin_x, h_origin_y]
            self.visited.add((h_origin_x, h_origin_y))

    def run(self):
        for instruction in self.instructions:
            self.move(instruction)


def process_input(blob):
    lines = blob.splitlines()
    instructions = []
    for line in lines:
        direction, steps = line.split(" ")
        instructions.append([direction, int(steps)])
    r = Rope(instructions)
    r.run()
    return r


def do_part_1(rope):
    return len(rope.visited)


def do_part_2(processed_input):
    return "toto"
