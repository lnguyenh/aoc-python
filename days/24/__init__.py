from collections import defaultdict

from utils.djikstra import djikstra


class Valley:
    def __init__(self, lines):
        self.start = (1, 0, 0)
        self.grid = {}
        self.blizzards = defaultdict(list)
        self.b = set()  # blizzard posiitions
        self.initialize(lines)
        self.min_x, self.max_x, self.min_y, self.max_y = self.get_maxes()
        self.destination = ((self.max_x - 1), self.max_y)

    def initialize(self, lines):
        for j, line in enumerate(lines):
            for i, c in enumerate(line):
                if c == "#":
                    self.grid[(i, j)] = c
                elif c != ".":
                    self.blizzards[c].append((i, j))
                    self.b.add((i, j))

    def get_maxes(self):
        xes = [x for x, _ in self.grid.keys()]
        yes = [y for _, y in self.grid.keys()]
        return min(xes), max(xes), min(yes), max(yes)

    def print(self):
        for y in range(self.min_y, self.max_y + 1):
            line = ""
            for x in range(self.min_x, self.max_x + 1):
                if self.grid.get((x, y)):
                    line += "#"
                elif (x, y) in self.b:
                    line += "B"
                else:
                    line += "."
            print(line)
        print("\n")

    def edges_for_n_minutes(self, n):
        edges = []
        for t in range(n):
            new_edges = []
            print(f"Minute {t}")
            self.print()
            toto = 1
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    point = (x, y)
                    if self.grid.get(point) or (point in self.b):
                        continue

                    new_edges.append(
                        ((x, y, t - 1), (x, y, t), 1)
                    )  # stay same position

                    origins = [
                        (x, y - 1),
                        (x - 1, y),
                        (x + 1, y),
                        (x, y + 1),
                    ]
                    for x2, y2 in origins:
                        if (x, y) == self.destination:
                            new_edges.append(((x2, y2, t - 1), (x, y), 1))
                        else:
                            new_edges.append(((x2, y2, t - 1), (x, y, t), 1))
            edges.extend(new_edges)

            self.move_blizzards()
        return edges

    def move_blizzards(self):
        new_blizzards = defaultdict(list)
        new_positions = set()
        for direction, positions in self.blizzards.items():
            for x, y in positions:
                if direction == ">":
                    y2 = y
                    x2 = x + 1 if x < self.max_x - 1 else 1
                elif direction == "<":
                    y2 = y
                    x2 = x - 1 if x > 1 else self.max_x - 1
                elif direction == "^":
                    x2 = x
                    y2 = y - 1 if y > 1 else self.max_y - 1
                elif direction == "v":
                    x2 = x
                    y2 = y + 1 if y < self.max_y - 1 else 1
                else:
                    raise Exception
                new_blizzards[direction].append((x2, y2))
                new_positions.add((x2, y2))
        self.blizzards = new_blizzards
        self.b = new_positions


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    valley = Valley(lines)
    edges = valley.edges_for_n_minutes(30)
    cost, path = djikstra(edges, valley.start, valley.destination)
    print(cost)
    print(path)
    return cost


def do_part_2(processed_input):
    return "toto"
