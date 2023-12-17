from utils.djikstra import djikstra
from utils.grid import Grid


class City(Grid):
    def __init__(self, lines, min_steps, max_steps):
        super().__init__(lines)
        self.min_steps = min_steps
        self.max_steps = max_steps
        self.edges = self.build_edges()

    def build_edges(self):
        edges = []
        for x, y in self.points:
            for direction in [(1, 0), (-1, 0)]:
                cost = 0
                for i in range(1, self.max_steps + 1):
                    point = (x, y)
                    destination = (x + i * direction[0], y + i * direction[1])
                    if self.grid.get(destination) is None:
                        continue
                    cost += int(self.grid[destination])
                    if i < self.min_steps:
                        continue
                    edges.append(((point, "v"), (destination, "h"), cost))
            for direction in [(0, 1), (0, -1)]:
                cost = 0
                for i in range(1, self.max_steps + 1):
                    point = (x, y)
                    destination = (x + i * direction[0], y + i * direction[1])
                    if self.grid.get(destination) is None:
                        continue
                    cost += int(self.grid[destination])
                    if i < self.min_steps:
                        continue
                    edges.append(((point, "h"), (destination, "v"), cost))
        return edges

    def get_shortest_path(self):
        return min(
            [
                djikstra(self.edges, ((0, 0), "h"), ((self.maxx, self.maxy), "h"))[0],
                djikstra(self.edges, ((0, 0), "h"), ((self.maxx, self.maxy), "v"))[0],
                djikstra(self.edges, ((0, 0), "v"), ((self.maxx, self.maxy), "h"))[0],
                djikstra(self.edges, ((0, 0), "v"), ((self.maxx, self.maxy), "v"))[0],
            ]
        )


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    city = City(lines, 1, 3)
    return city.get_shortest_path()


def do_part_2(lines):
    city = City(lines, 4, 10)
    return city.get_shortest_path()


def do_visualization(processed_input):
    return None
