from itertools import cycle


def process_input(blob):
    instructions, raw_patterns = blob.split("\n\n")

    patterns = {}
    for raw_pattern in raw_patterns.split("\n"):
        tmp = raw_pattern.replace(" = (", ":")
        tmp = tmp.replace(", ", ":")
        tmp = tmp.replace(")", "")
        origin, left, right = tmp.split(":")
        patterns[(origin, "L")] = left
        patterns[(origin, "R")] = right

    return instructions, patterns


def do_part_1(processed_input):
    instructions, patterns = processed_input
    infinite_instructions = cycle(instructions)

    node = "AAA"
    count = 0
    while node != "ZZZ":
        lr = next(infinite_instructions)
        node = patterns[(node, lr)]
        count += 1

    return count


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
