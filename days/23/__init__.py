from collections import defaultdict


class Field:
    def __init__(self, lines):
        self.grid = {}
        self.populate_grid(lines)
        self.direction = 0

        self.candidates = {}

    def populate_grid(self, lines):
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == "#":
                    self.grid[(i, j)] = "#"

    def change_first_direction(self):
        self.direction = (self.direction + 1) % 4  # 0: N, 1: S, 2: W, 3: E

    def get_next_direction(self, direction):
        return (direction + 1) % 4

    def play_n_rounds(self, n):
        # self.print()
        for i in range(n):
            # print(f"Round #{i+1} (starting direction: {self.direction})")
            self.play_one_round()
            # self.print()

    def play_until_no_move(self):
        turn = 1
        while True:
            if self.play_one_round() == 0:
                break
            turn += 1
        return turn

    def play_one_round(self):
        self.candidates = {}
        direction = self.direction

        movable_elves = set(self.grid.keys())
        immobile_elves = set()
        candidates = defaultdict(list)

        for x, y in movable_elves:
            around = [
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
            ]
            if any([self.grid.get((xx, yy)) for xx, yy in around]):
                continue
            immobile_elves.add((x, y))

        for x, y in immobile_elves:
            movable_elves.remove((x, y))

        toto = 0

        # Populate candidates
        for _ in range(4):
            can_move_in_this_direction = []
            for x, y in movable_elves:
                possible_move = self.can_move((x, y), direction)
                if possible_move is not None:
                    candidates[possible_move].append((x, y))
                    can_move_in_this_direction.append((x, y))
            for x, y in can_move_in_this_direction:
                movable_elves.remove((x, y))
            direction = self.get_next_direction(direction)

        num_moves = 0

        # Move if possible
        for destination, elves in candidates.items():
            if len(elves) == 1:
                elf = elves[0]
                self.move_elf(elf, destination)
                num_moves += 1

        # Change the first direction
        self.change_first_direction()

        return num_moves

    def move_elf(self, elf, destination):
        self.grid.pop(elf)
        self.grid[destination] = "#"

    def print(self):
        xes = [a[0] for a in self.grid.keys()]
        yes = [a[1] for a in self.grid.keys()]
        x_min = min(xes)
        x_max = max(xes)
        y_min = min(yes)
        y_max = max(yes)

        for y in range(y_min, y_max + 1):
            line = ""
            for x in range(x_min, x_max + 1):
                line += self.grid.get((x, y), ".")
            print(line)
        print("\n")

    def get_result(self):
        xes = [a[0] for a in self.grid.keys()]
        yes = [a[1] for a in self.grid.keys()]
        x_min = min(xes)
        x_max = max(xes)
        y_min = min(yes)
        y_max = max(yes)

        count = 0

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if not self.grid.get((x, y)):
                    count += 1

        return count

    def can_move(self, elf, direction):
        x, y = elf
        if direction == 0:
            # N
            possibles = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        elif direction == 1:
            # S
            possibles = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        elif direction == 2:
            # W
            possibles = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        elif direction == 3:
            possibles = [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        else:
            raise Exception("unknown direction")

        if any([self.grid.get((xx, yy)) for xx, yy in possibles]):
            return None

        return possibles[1]


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    field = Field(lines)
    field.play_n_rounds(10)
    return field.get_result()


def do_part_2(lines):
    field = Field(lines)
    return field.play_until_no_move()
