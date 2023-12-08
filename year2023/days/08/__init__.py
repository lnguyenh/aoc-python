from itertools import cycle
from math import lcm


def process_input(blob):
    instructions, raw_patterns = blob.split("\n\n")

    patterns = {}
    nodes = []
    for raw_pattern in raw_patterns.split("\n"):
        tmp = raw_pattern.replace(" = (", ":")
        tmp = tmp.replace(", ", ":")
        tmp = tmp.replace(")", "")
        origin, left, right = tmp.split(":")
        patterns[(origin, "L")] = left
        patterns[(origin, "R")] = right
        nodes.append(origin)

    return instructions, patterns, nodes


def do_part_1(processed_input):
    instructions, patterns, _ = processed_input
    infinite_instructions = cycle(instructions)
    node = "AAA"
    count = 0
    while node != "ZZZ":
        lr = next(infinite_instructions)
        node = patterns[(node, lr)]
        count += 1
    return count


def do_part_2(processed_input):
    instructions, patterns, nodes = processed_input
    a_nodes = [node for node in nodes if node.endswith("A")]

    jumps = {}
    for node in nodes:
        infinite_instructions = cycle(instructions)

        position = node
        count = 0
        while True:
            lr = next(infinite_instructions)

            # Break for dead nodes like XXX = (XXX, XXX)
            if patterns[(position, "R")] == patterns[(position, "L")] == position:
                break

            position = patterns[(position, lr)]
            count += 1

            if position.endswith("Z") or position == node:
                break
        jumps[node] = (count, position)

    useful_jumps = {
        node: value for node, value in jumps.items() if value[1].endswith("Z")
    }

    coefficients = [useful_jumps[node][0] for node in a_nodes]

    return lcm(*coefficients)
