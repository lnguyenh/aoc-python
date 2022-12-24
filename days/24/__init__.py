from collections import defaultdict

from utils.djikstra import djikstra

N = 300


class Valley:
    def __init__(self, lines):
        self.grid = {}
        self.blizzards = defaultdict(list)
        self.b = set()  # blizzard posiitions
        self.initialize(lines)
        self.min_x, self.max_x, self.min_y, self.max_y = self.get_maxes()

        self.p1 = (1, 0)
        self.p2 = ((self.max_x - 1), self.max_y)

        self.destination = self.p2

        self.one_way = 0

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
            # print(f"Minute {t}")
            # self.print()
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
    lines = blob.split("\n")
    return Valley(lines), lines


def do_part_1(processed_input):
    valley, _ = processed_input
    edges = valley.edges_for_n_minutes(280)
    cost, path = djikstra(edges, (1, 0, 0), valley.destination)
    # print(cost)
    # print(path)
    return cost


def do_part_2(processed_input):
    _, lines = processed_input
    valley1 = Valley(lines)
    valley2 = Valley(lines)
    valley3 = Valley(lines)

    # Go
    valley1.destination = valley1.p2
    edges = valley1.edges_for_n_minutes(N)
    cost, path = djikstra(edges, valley1.p1 + (0,), valley1.destination)
    # print(cost)
    # print(path)
    step1 = int(cost) + 1

    # Back
    valley2.destination = valley2.p1
    _ = valley2.edges_for_n_minutes(step1)
    edges = valley2.edges_for_n_minutes(N)
    cost, path = djikstra(edges, valley2.p2 + (0,), valley2.destination)
    # print(cost)
    # print(path)
    step2 = int(cost) + step1

    # Go
    valley3.destination = valley3.p2
    _ = valley3.edges_for_n_minutes(step2)
    edges = valley3.edges_for_n_minutes(N)
    cost, path = djikstra(edges, valley3.p1 + (0,), valley3.destination)
    # print(cost)
    # print(path)

    return step2 + cost
