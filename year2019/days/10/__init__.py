from collections import defaultdict, deque
from itertools import zip_longest, chain

from math import gcd, atan2, degrees
import operator

from utils.grid import Grid


class Field(Grid):
    SKIP = (".",)

    def __init__(self, lines):
        super().__init__(lines)

    def max_num_vectors(self):
        max_vectors = 0
        asteroid = None
        for i, j in self.points:
            vectors = set()
            for i2, j2 in self.points:
                if (i2, j2) == (i, j):
                    continue
                divisor = gcd(i2 - i, j2 - j)
                vector = ((i2 - i) / divisor, (j2 - j) / divisor)
                vectors.add(vector)
            num_vectors = len(vectors)
            if num_vectors > max_vectors:
                max_vectors = num_vectors
                asteroid = (i, j)
        return asteroid, max_vectors

    def build_clockwise_sorted_points_from_center(self, center):
        i, j = center
        asteroid_map = defaultdict(list)
        for i2, j2 in self.points:
            if (i2, j2) == (i, j):
                continue
            divisor = gcd(i2 - i, j2 - j)
            vector = ((i2 - i) // divisor, (j2 - j) // divisor)
            asteroid_map[vector].append((i2 - i, j2 - j))
        for key, asteroids in asteroid_map.items():
            asteroid_map[key] = sorted(
                asteroids, key=lambda x: abs(x[0]) * abs(x[0]) + abs(x[1]) * abs(x[1])
            )
        directions = asteroid_map.keys()

        # https://stackoverflow.com/questions/51074984/sorting-according-to-clockwise-point-coordinates
        center = (0, 0)
        # ANTI clockwise compared to the stack overflow answer because of how our axes are
        sorted_directions = deque(
            sorted(
                directions,
                key=lambda coord: -(
                    -135
                    - degrees(atan2(*tuple(map(operator.sub, coord, center))[::-1]))
                )
                % 360,
            )
        )
        while sorted_directions[0] != (0, -1):
            sorted_directions.rotate(-1)

        sorted_points = [asteroid_map[d] for d in list(sorted_directions)]
        sorted_points = [
            (point[0] + i, point[1] + j)
            for point in chain(*zip_longest(*sorted_points))
            if point is not None
        ]

        return sorted_points


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    field = Field(lines)
    _, num_detections = field.max_num_vectors()
    return num_detections


def do_part_2(lines):
    field = Field(lines)
    center, _ = field.max_num_vectors()
    points = field.build_clockwise_sorted_points_from_center(center)
    x, y = points[199]
    return 100 * x + y


def do_visualization(processed_input):
    return None
