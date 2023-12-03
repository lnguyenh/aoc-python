import re
from collections import defaultdict

from utils.grid import Grid


def process_input(blob):
    return Engine(blob.split("\n"))


class Engine(Grid):
    def __init__(self, lines):
        self.lines = self.transform_lines(lines)
        super().__init__(self.lines)
        self.numbers = self.extract_numbers()

    def transform_lines(self, lines):
        # reduce the number of possible symbols to make things easier afterwards
        new_lines = []
        for line in lines:
            characters = []
            for c in line:
                if c.isdigit() or c == "." or c == "*":
                    characters.append(c)
                else:
                    characters.append("#")
            new_lines.append("".join(characters))
        return new_lines

    def extract_numbers(self):
        numbers = []
        for j, line in enumerate(self.lines):
            number_candidates = re.split("[.|#|*]", line)
            i = 0  # cursor to keep track of where we are on each line
            for number in number_candidates:
                length = len(number)
                if len(number) > 0:
                    # create list of all surrounding points coordinates
                    surroundings = []
                    for x in range(i - 1, i + length + 1):
                        surroundings.append((x, j - 1))
                        surroundings.append((x, j + 1))
                    surroundings.append((i - 1, j))
                    surroundings.append((i + length, j))
                    numbers.append((int(number), surroundings))
                    i += length + 1
                else:
                    i += 1
        return numbers

    def do_part_1(self):
        total = 0
        for number, points in self.numbers:
            for x, y in points:
                if self.grid.get((x, y)) in ["#", "*"]:
                    total += number
                    break
        return total

    def do_part_2(self):
        possible_gears = []
        for j, line in enumerate(self.lines):
            for i, c in enumerate(line):
                if c == "*":
                    possible_gears.append((i, j))

        gears_and_numbers = defaultdict(list)
        for gear in possible_gears:
            for number, surroundings in self.numbers:
                if gear in surroundings:
                    gears_and_numbers[gear].append(number)

        count = 0
        for _, numbers in gears_and_numbers.items():
            if len(numbers) == 2:
                count += numbers[0] * numbers[1]
        return count


def do_part_1(engine):
    return engine.do_part_1()


def do_part_2(engine):
    return engine.do_part_2()
