from collections import deque, defaultdict

from utils.grid import Grid


SLASH_REFLECTIONS = {
    (0, 1): (-1, 0),
    (0, -1): (1, 0),
    (1, 0): (0, -1),
    (-1, 0): (0, 1),
}

BACKSLASH_REFLECTIONS = {
    (0, 1): (1, 0),
    (0, -1): (-1, 0),
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
}


def add_to_deque(point, p, direction, paths, illumination):
    new_p = p[:]
    new_p.append(point)
    paths.append((point, direction, new_p))
    illumination[point].append(direction)


class Maze(Grid):
    def __init__(self, lines):
        super().__init__(lines)

    def is_dead_end(self, point, direction, illumination):
        return not self.is_in_bounds(point) or direction in illumination.get(point, [])

    def get_illumination(self, p0, d0):

        paths = deque()
        paths.append((p0, d0, [p0]))  # current point, direction, path

        illumination = defaultdict(list)
        illumination[p0].append(d0)

        full_paths = []
        while paths:
            path = paths.pop()

            [point, direction, p] = path
            x, y = point

            v = self.grid.get(point)
            if (
                v == "."
                or (v == "|" and direction in [(0, 1), (0, -1)])
                or (v == "-" and direction in [(1, 0), (-1, 0)])
            ):
                new_point = (x + direction[0], y + direction[1])
                if self.is_dead_end(new_point, direction, illumination):
                    full_paths.append(p[:])
                    continue
                add_to_deque(new_point, p, direction, paths, illumination)
            elif v == "|":
                for new_direction in [(0, 1), (0, -1)]:
                    new_point = (x + new_direction[0], y + new_direction[1])
                    if self.is_dead_end(new_point, new_direction, illumination):
                        full_paths.append(p[:])
                        continue
                    add_to_deque(new_point, p, new_direction, paths, illumination)
            elif v == "-":
                for new_direction in [(1, 0), (-1, 0)]:
                    new_point = (x + new_direction[0], y + new_direction[1])
                    if self.is_dead_end(new_point, new_direction, illumination):
                        full_paths.append(p[:])
                        continue
                    add_to_deque(new_point, p, new_direction, paths, illumination)
            elif v == "/":
                new_direction = SLASH_REFLECTIONS[direction]
                new_point = (x + new_direction[0], y + new_direction[1])
                if self.is_dead_end(new_point, new_direction, illumination):
                    full_paths.append(p[:])
                    continue
                add_to_deque(new_point, p, new_direction, paths, illumination)
            elif v == "\\":
                new_direction = BACKSLASH_REFLECTIONS[direction]
                new_point = (x + new_direction[0], y + new_direction[1])
                if self.is_dead_end(new_point, new_direction, illumination):
                    full_paths.append(p[:])
                    continue
                add_to_deque(new_point, p, new_direction, paths, illumination)
            else:
                raise Exception
        return illumination

    def do_part_1(self):
        return len(self.get_illumination((0, 0), (1, 0)).keys())

    def do_part_2(self):
        current_max = 0
        starts = []
        for i in range(self.minx, self.maxx + 1):
            starts.append(((i, self.miny), (0, 1)))
            starts.append(((i, self.maxy), (0, -1)))
        for j in range(self.miny, self.maxy + 1):
            starts.append(((self.minx, j), (1, 0)))
            starts.append(((self.maxx, j), (-1, 0)))

        for p, d in starts:
            intensity = len(self.get_illumination(p, d).keys())
            if intensity > current_max:
                current_max = intensity

        return current_max


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    maze = Maze(lines)
    return maze.do_part_1()


def do_part_2(lines):
    maze = Maze(lines)
    return maze.do_part_2()


def do_visualization(processed_input):
    return None
