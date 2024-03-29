import heapq
from collections import defaultdict
from functools import cached_property


class Brick:
    def __init__(self, name, line):
        p0, p1 = line.split("~")
        x0, y0, z0 = p0.split(",")
        x1, y1, z1 = p1.split(",")

        assert x0 <= x1
        assert z0 <= z1
        assert y0 <= y1

        self.name = name
        self.p0 = (int(x0), int(y0))
        self.p1 = (int(x1), int(y1))
        self.z0 = int(z0)
        self.z1 = int(z1)

        self.zs = None
        self.z = None
        self.set_zs(self.z0)

    @cached_property
    def xy_points(self):
        points = []
        for x in range(self.p0[0], self.p1[0] + 1):
            for y in range(self.p0[1], self.p1[1] + 1):
                points.append((x, y))
        return set(points)

    def set_zs(self, z):
        self.z = z
        self.zs = list(range(z, z + (self.z1 - self.z0) + 1))


def process_input(blob):
    bricks = [Brick(f"B{i}", line) for i, line in enumerate(blob.split("\n"))]
    return bricks


def do_part_1(bricks):

    while True:
        num = 0
        for brick in bricks:
            if 1 in brick.zs:
                continue
            layer_below = brick.z - 1
            points_occupied = set()
            for b in bricks:
                if layer_below in b.zs:
                    points_occupied.update(b.xy_points)
            if not brick.xy_points.intersection(points_occupied):
                brick.set_zs(layer_below)
                num += 1
        if not num:
            break

    supported_by = defaultdict(set)
    supports = defaultdict(set)
    answer = set()
    for brick in bricks:
        layer_above = max(brick.zs) + 1
        bricks_above = []
        for b in bricks:
            if layer_above in b.zs and b.name != brick.name:
                if brick.xy_points.intersection(b.xy_points):
                    bricks_above.append(b.name)
                    supported_by[b.name].add(brick.name)
                    supports[brick.name].add(b.name)
        if not bricks_above:
            answer.add(brick.name)

    names = set([b.name for b in bricks])

    for brick in bricks:
        for name, by in supported_by.items():
            if by == {brick.name}:
                names.discard(brick.name)
    return len(names)

    return len(answer)


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
