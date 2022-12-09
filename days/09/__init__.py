import os
from itertools import product
from time import sleep

NUM_KNOTS = 10  # including head


def too_far(k1, k2):
    x_diff = abs(k1[0] - k2[0])
    y_diff = abs(k1[1] - k2[1])
    return x_diff > 1 or y_diff > 1


class Rope:
    def __init__(self, instructions):
        self.instructions = instructions
        self.h = (0, 0)
        self.t = (0, 0)
        self.visited = {(0, 0)}
        self.knots = [(0, 0)] * NUM_KNOTS

    def print(self):
        os.system("clear" if os.name == "posix" else "CLS")
        coordinates = {}
        for i, point in enumerate(self.knots):
            if not coordinates.get(point):
                coordinates[point] = "H" if i == 0 else str(i)
        for y in range(30, -15, -1):
            line = ""
            for x in range(-40, 40 + 1):
                line = line + coordinates.get((x, y), ".")
            print(line)
        sleep(0.05)

    def move_head(self, direction):
        x, y = self.h
        if direction == "R":
            self.h = (x + 1, y)
        elif direction == "L":
            self.h = (x - 1, y)
        elif direction == "U":
            self.h = (x, y + 1)
        elif direction == "D":
            self.h = (x, y - 1)
        self.knots[0] = (self.h[0], self.h[1])
        return x, y

    def move(self, instruction):
        direction, steps = instruction
        for _ in range(steps):
            h_original_x, h_original_y = self.move_head(direction)
            self.move_tail(h_original_x, h_original_y)

    def move_tail(self, h_origin_x, h_origin_y):
        x_diff = abs(self.h[0] - self.t[0])
        y_diff = abs(self.h[1] - self.t[1])
        if x_diff > 1 or y_diff > 1:
            self.t = [h_origin_x, h_origin_y]
            self.visited.add((h_origin_x, h_origin_y))

    def run(self):
        for instruction in self.instructions:
            self.move(instruction)

    def find_vector(self, i, picky=True):
        prev_x, prev_y = self.knots[i - 1]
        for delta_x, delta_y in product([-1, 0, 1], [-1, 0, 1]):
            if too_far(
                (
                    self.knots[i][0] + delta_x,
                    self.knots[i][1] + delta_y,
                ),
                self.knots[i - 1],
            ):
                continue
            if not picky:
                return delta_x, delta_y
            if (
                self.knots[i][0] + delta_x == prev_x
                or self.knots[i][1] + delta_y == prev_y
            ):
                return delta_x, delta_y
        return self.find_vector(i, picky=False)

    def move2(self, instruction):
        direction, steps = instruction
        for _ in range(steps):
            for i in range(NUM_KNOTS):
                if i == 0:
                    self.move_head(direction)
                else:
                    if too_far(self.knots[i], self.knots[i - 1]):
                        # Move
                        dx, dy = self.find_vector(i)
                        self.knots[i] = (self.knots[i][0] + dx, self.knots[i][1] + dy)

                        # Keep track of visited points by tail
                        if i == NUM_KNOTS - 1:
                            self.visited.add(self.knots[i])
                            break

                    else:
                        break
            # Uncomment to print all steps
            # self.print()

    def run2(self):
        for instruction in self.instructions:
            self.move2(instruction)


def process_input(blob):
    lines = blob.splitlines()
    instructions = []
    for line in lines:
        direction, steps = line.split(" ")
        instructions.append([direction, int(steps)])
    r1 = Rope(instructions)
    r2 = Rope(instructions)
    return r1, r2


def do_part_1(ropes):
    r, _ = ropes
    r.run()
    return len(r.visited)


def do_part_2(ropes):
    _, r = ropes
    r.run2()
    return len(r.visited)
