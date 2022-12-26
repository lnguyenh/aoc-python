from fractions import Fraction
from math import gcd

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


def process_input(blob):
    return blob.split("\n")


def do_part_1(lines):
    field = Field(lines)
    asteroid, num_detections = field.max_num_vectors()
    return num_detections


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
