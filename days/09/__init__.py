NUM_KNOTS = 10  # including head


class Rope:
    def __init__(self, instructions):
        self.instructions = instructions
        self.h = (0, 0)
        self.t = (0, 0)
        self.visited = {(0, 0)}
        self.knots = [
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ]
        self.memory = [
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        ]

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

    def print(self):
        xs = [a[0] for a in self.knots]
        ys = [a[1] for a in self.knots]
        coordinates = {}
        for i, point in enumerate(self.knots):
            if not coordinates.get(point):
                coordinates[point] = "H" if i == 0 else str(i)
        minx = min(xs)
        miny = min(ys)
        maxx = max(xs)
        maxy = max(ys)
        z = 1
        for y in range(maxy, miny - 1, -1):
            line = ""
            for x in range(minx, maxx + 1):
                line = line + coordinates.get((x, y), ".")
            print(line)
        print("\n")

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

    def move2(self, instruction):
        direction, steps = instruction
        for _ in range(steps):
            self.print()
            dx, dy = 0, 0

            for i in range(NUM_KNOTS):
                self.memory[i] = self.knots[i]
                if i == 0:
                    self.move_head(direction)
                    dx, dy = (
                        self.memory[i][0] - self.knots[i + 1][0],
                        self.memory[i][1] - self.knots[i + 1][1],
                    )
                else:
                    x_diff = abs(self.knots[i][0] - self.knots[i - 1][0])
                    y_diff = abs(self.knots[i][1] - self.knots[i - 1][1])
                    if x_diff > 1 or y_diff > 1:

                        # We need to move
                        self.knots[i] = (self.knots[i][0] + dx, self.knots[i][1] + dy)

                        # Tail
                        if i == NUM_KNOTS - 1:
                            self.visited.add(self.knots[i])
                            break

                        # If next knot is at a diagonal compared to us, we change the dx
                        if (
                            self.memory[i][0] - self.knots[i + 1][0] != 0
                            and self.memory[i][1] - self.knots[i + 1][1] != 0
                        ):
                            dx, dy = (
                                self.memory[i][0] - self.knots[i + 1][0],
                                self.memory[i][1] - self.knots[i + 1][1],
                            )

                    else:
                        break

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
