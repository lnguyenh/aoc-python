import re


class MonkeyMap:
    def __init__(self, text, instructions):
        self.grid = {}
        self.instructions = instructions
        self.start = None
        self.position = None

        self.max_i = 0
        self.max_j = 0

        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.populate_grid(text)

    def populate_grid(self, text):
        for j, line in enumerate(text.split("\n")):
            self.max_j = j
            for i, c in enumerate(line):
                self.max_i = max(i, self.max_i)
                if c != " ":
                    self.grid[(i, j)] = c
                if self.start is None and c == ".":
                    self.start = (i, j)
                    self.position = (i, j)

    def move(self, steps):
        next_position = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for _ in range(steps):
            self.position = self.get_next_position(next_position[self.direction])
            toti = 1

    def get_next_position(self, vector):
        candidate = (self.position[0] + vector[0], self.position[1] + vector[1])
        while True:
            if self.grid.get(candidate):
                if self.grid[candidate] == "#":
                    return self.position
                else:
                    return candidate
            candidate = (candidate[0] + vector[0], candidate[1] + vector[1])
            if candidate[0] > self.max_i:
                candidate = (0, candidate[1])
            elif candidate[0] < 0:
                candidate = (self.max_i, candidate[1])

            if candidate[1] > self.max_j:
                candidate = (candidate[0], 0)
            elif candidate[1] < 0:
                candidate = (candidate[0], self.max_j)

    def rotate(self, letter):
        if letter == "R":
            self.direction = (self.direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4

    def run(self):
        for instr in self.instructions:
            if type(instr) == int:
                self.move(instr)
            else:
                self.rotate(instr)
            # self.print()
            toto = 1

    def get_part_1(self):
        column = self.position[0] + 1
        row = self.position[1] + 1
        direction = self.direction
        return 1000 * row + 4 * column + direction

    def print(self):
        for j in range(self.max_j + 1):
            line = ""
            for i in range(self.max_i + 1):
                if (i, j) == self.position:
                    line = line + f"{self.direction}"
                else:
                    line = line + self.grid.get((i, j), " ")
            print(line)
        print("\n")


def process_input(blob):
    map_points, instructions = blob.split("\n\n")
    reg = re.compile("([0-9]+)([a-zA-Z]?)")
    instructions = reg.findall(instructions)
    final_instructions = []
    for a, b in instructions:
        final_instructions.append(int(a))
        if b:
            final_instructions.append(b)
    return MonkeyMap(map_points, final_instructions)


def do_part_1(monkey_map):
    # monkey_map.print()
    monkey_map.run()
    return monkey_map.get_part_1()


def do_part_2(processed_input):
    return "toto"
