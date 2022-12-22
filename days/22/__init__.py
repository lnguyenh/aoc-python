import re


class MonkeyMap:
    def __init__(self, text, instructions, mode):
        self.grid = {}
        self.mode = mode
        self.instructions = instructions
        self.start = None
        self.position = None

        self.max_i = 0
        self.max_j = 0

        self.w = 6000  # Just something bigger than the real width

        self.real_direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.populate_grid(text)

        self.seen = set()

    def populate_grid(self, text):
        for j, line in enumerate(text.split("\n")):
            self.w = min([self.w, len(line.replace(" ", ""))])
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
            if self.mode == 1:
                self.position = self.get_next_position_1(
                    next_position[self.real_direction]
                )
            else:
                self.position = self.get_next_position_2(
                    next_position[self.real_direction]
                )

    def get_next_position_1(self, vector):
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

    def get_next_position_2(self, vector):
        w = self.w
        old_x, old_y = self.position
        saved_real_direction = self.real_direction

        candidate = (self.position[0] + vector[0], self.position[1] + vector[1])
        x, y = candidate
        policy = "standard"

        # Completely custom for my real input "shape". Will not work for test input
        if not self.grid.get(candidate):
            policy = None
            if x <= (2 * w - 1) and y == -1 and old_y == 0:
                # A
                self.rotate_real(1)
                candidate = (0, x + 2 * w)
                policy = "A"
            elif x == -1 and y >= 3 * w:
                # A'
                self.rotate_real(3)
                candidate = (y - 2 * w, 0)
                policy = "A'"
            elif y == 2 * w - 1 and old_y == 2 * w:
                # B
                self.rotate_real(1)
                candidate = (w, x + w)
                policy = "B"
            elif x == w - 1 and y >= w and old_x == w:
                # B'
                self.rotate_real(3)
                candidate = (y - w, 2 * w)
                policy = "B'"
            elif x == 2 * w and old_x == 2 * w - 1 and y < (2 * w):
                # C
                self.rotate_real(3)
                candidate = (y + w, w - 1)
                policy = "C"
            elif y == w and old_y == (w - 1):
                # C'
                self.rotate_real(1)
                candidate = (2 * w - 1, x - w)
                policy = "C'"
            elif x == w and old_x == w - 1:
                # D
                self.rotate_real(3)
                candidate = (y - 2 * w, 3 * w - 1)
                policy = "D"
            elif y == 3 * w and old_y == 3 * w - 1:
                # D'
                self.rotate_real(1)
                candidate = (w - 1, 2 * w + x)
                policy = "D'"
            elif x == w - 1 and y <= (w - 1):
                # E
                self.rotate_real(2)
                candidate = (0, 2 * w + (w - 1 - y))
                policy = "E"
            elif x == -1 and y < 3 * w:
                # E'
                self.rotate_real(2)
                candidate = (w, (w - 1) - (y - 2 * w))
                policy = "E'"
            elif x == 2 * w and y >= 2 * w:
                # F
                self.rotate_real(2)
                candidate = (3 * w - 1, (w - 1) - (y - 2 * w))
                policy = "F"
            elif x == 3 * w:
                # F'
                self.rotate_real(2)
                candidate = (2 * w - 1, 2 * w + (w - 1 - y))
                policy = "F'"
            elif y == -1 and x >= 2 * w:
                # G
                candidate = (x - 2 * w, 4 * w - 1)
                policy = "G"
            elif y >= 4 * w:
                # G'
                candidate = (2 * w + x, 0)
                policy = "G'"
            else:
                raise Exception

        if policy not in self.seen:
            self.seen.add(policy)
            # print(
            #     f"old ({old_x},{old_y}) (d: {saved_real_direction}) - first_candidate ({x}.{y}) - cube candidate {candidate} (d: {self.real_direction}) - policy {policy}"
            # )

        if self.grid[candidate] == "#":
            self.real_direction = saved_real_direction
            return self.position
        else:
            return candidate

    def rotate(self, letter):
        if letter == "R":
            self.direction = (self.direction + 1) % 4
            self.real_direction = (self.real_direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4
            self.real_direction = (self.real_direction - 1) % 4

    def rotate_real(self, num):
        for _ in range(num):
            self.real_direction = (self.real_direction + 1) % 4

    def run(self):
        for instr in self.instructions:
            if type(instr) == int:
                self.move(instr)
            else:
                self.rotate(instr)

    def get_answer(self):
        column = self.position[0] + 1
        row = self.position[1] + 1
        direction = self.direction if self.mode == 1 else self.real_direction
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
    return blob


def get_monkey_map(blob, mode):
    map_points, instructions = blob.split("\n\n")
    reg = re.compile("([0-9]+)([a-zA-Z]?)")
    instructions = reg.findall(instructions)
    final_instructions = []
    for a, b in instructions:
        final_instructions.append(int(a))
        if b:
            final_instructions.append(b)
    return MonkeyMap(map_points, final_instructions, mode)


def do_part_1(blob):
    monkey_map = get_monkey_map(blob, mode=1)
    monkey_map.run()
    return monkey_map.get_answer()


def do_part_2(blob):
    monkey_map = get_monkey_map(blob, mode=2)
    monkey_map.run()
    return monkey_map.get_answer()
