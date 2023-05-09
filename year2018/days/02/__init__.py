from collections import defaultdict
from itertools import combinations


def process_input(blob):
    return blob.split("\n")


def do_part_1(boxes):
    twos = 0
    threes = 0
    for box in boxes:
        stat = defaultdict(int)
        for c in box:
            stat[c] += 1
        if any([count == 2 for _, count in stat.items()]):
            twos += 1
        if any([count == 3 for _, count in stat.items()]):
            threes += 1
    return twos * threes


def merge_names(name_1, name_2):
    merged_name = ""
    false_counter = 0
    for i, _ in enumerate(name_1):
        if name_1[i] == name_2[i]:
            merged_name += name_1[i]
        else:
            false_counter += 1
            if false_counter == 2:
                return ""
    return merged_name


def do_part_2(boxes):
    for name_1, name_2 in combinations(boxes, 2):
        merged_name = merge_names(name_1, name_2)
        if merged_name:
            return merged_name
    return "not found"


def do_visualization(processed_input):
    return None
