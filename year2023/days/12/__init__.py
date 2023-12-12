import itertools
from collections import deque


class Row:
    def __init__(self, phrase, arrangement):
        self.phrase = phrase
        self.arrangement = [int(c) for c in arrangement.split(",")]
        self.num_springs = len(self.phrase)
        self.num_broken = sum(self.arrangement)
        self.num_working = self.num_springs - self.num_broken

    def allows(self, candidate):
        for i in range(len(self.phrase)):
            if self.phrase[i] == "?":
                continue
            elif self.phrase[i] != candidate[i]:
                return False
        return True

    def get_combinations(self):
        blob = []
        max_consecutive_dots = self.num_springs - self.num_broken + 1
        blob.append(list(range(max_consecutive_dots)))
        for _ in range(len(self.arrangement) - 1):
            blob.append(list(range(1, max_consecutive_dots)))
        blob.append(list(range(max_consecutive_dots)))
        combinations = [
            p for p in itertools.product(*blob) if sum(p) == self.num_working
        ]

        return combinations

    def generate_candidate(self, combination):
        text = ""
        for i, num in enumerate(combination[:-1]):
            text += num * "."
            text += self.arrangement[i] * "#"
        text += combination[-1] * "."
        return text

    def count_allowed_candidates(self):
        total = 0
        for combination in self.get_combinations():
            candidate = self.generate_candidate(combination)
            if self.allows(candidate):
                total += 1
        return total


def process_input(blob):
    return [line.split(" ") for line in blob.split("\n")]


def do_part_1(lines):
    total = 0
    for phrase, arrangement in lines:
        row = Row(phrase, arrangement)
        total += row.count_allowed_candidates()
    return total


def do_part_2(lines):
    return "toto"


def do_visualization(processed_input):
    return None
