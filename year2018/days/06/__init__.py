import operator
from collections import defaultdict
from functools import lru_cache


def process_input(blob):
    blob = blob.replace(" ", "")
    return [tuple(map(int, line.split(","))) for line in blob.split("\n")]


@lru_cache
def manhattan(points):
    (x0, y0), (x1, y1) = points
    return abs(x0 - x1) + abs(y0 - y1)


def get_bounds(point, points):
    x0, y0 = point

    bounds = []
    conditions = [
        (operator.gt, operator.gt),
        (operator.lt, operator.lt),
        (operator.lt, operator.gt),
        (operator.gt, operator.lt),
    ]

    for condition in conditions:
        bound = None
        distance = None
        for x, y in points:
            if condition[0](x, x0) and condition[1](y, y0):
                d = manhattan(((x, y), (x0, y0)))
                if not bound or d < distance:
                    bound = (x, y)
                    distance = d
        if bound:
            bounds.append(bound)

    return bounds


def do_part_1(coordinates):
    # TODO NOT FINISHED
    for x, y in coordinates:
        bounds = get_bounds((x, y), coordinates)
        if len(bounds) == 4:
    return "toto"


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
