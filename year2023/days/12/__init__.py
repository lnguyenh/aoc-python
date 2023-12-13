import itertools
import re
from functools import lru_cache


@lru_cache
def process(phrase, arrangement):
    if not phrase:
        return 1 if not arrangement else 0

    # no group to find
    if not arrangement:
        if phrase.count("#") > 0:
            return 0
        return 1

    target = arrangement[0]

    # not enough characters to satisfy next target
    if target > len(phrase):
        return 0

    # try to find target
    reg = re.compile(r"[\?#]{" + str(target) + r"}($|\.|\?)")
    match = reg.match(phrase)
    if match:
        first_after_match = match.end(0)
        if phrase[0] == "?":
            return process(phrase[first_after_match:], arrangement[1:]) + process(
                phrase[1:], arrangement
            )
        else:
            return process(phrase[first_after_match:], arrangement[1:])

    # if we find a # at the start it must be too few
    if phrase[0] == "#":
        return 0

    return process(phrase[1:], arrangement)


class Row:
    def __init__(self, phrase, arrangement):
        self.phrase_5 = "?".join([phrase, phrase, phrase, phrase, phrase])
        self.arrangement_5 = tuple([int(c) for c in arrangement.split(",")]) * 5
        self.phrase = phrase
        self.arrangement = tuple([int(c) for c in arrangement.split(",")])
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
        x = process(row.phrase, row.arrangement)
        total += x
    return total


def do_part_2(lines):
    total = 0
    for phrase, arrangement in lines:
        row = Row(phrase, arrangement)
        x = process(row.phrase_5, row.arrangement_5)
        total += x
    return total


def do_visualization(processed_input):
    return None


if __name__ == "__main__":
    print(process("?###????????", [3, 2, 1]))
    print(process("????.######..#####. 1,6,5", [1, 6, 5]))
