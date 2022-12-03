import string


def priority(character):
    offset = 26 if character.isupper() else 0
    return string.ascii_lowercase.index(character.lower()) + 1 + offset


def process_input(blob):
    return [[priority(c) for c in line] for line in blob.split("\n")]


def do_part_1(lines):
    priority_sum = 0
    for line in lines:
        length = int(len(line) / 2)
        common = {*line[:length]}.intersection({*line[length:]}).pop()
        priority_sum += common
    return priority_sum


def do_part_2(lines):
    priority_sum = 0
    for i in range(0, len(lines), 3):
        a, b, c = lines[i], lines[i + 1], lines[i + 2]
        common = set(a).intersection(set(b)).intersection(set(c)).pop()
        priority_sum += common
    return priority_sum
