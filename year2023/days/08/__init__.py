from itertools import cycle


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
    return "toto"
    instructions, patterns, _ = processed_input
    infinite_instructions = cycle(instructions)
    node = "AAA"
    count = 0
    while node != "ZZZ":
        lr = next(infinite_instructions)
        node = patterns[(node, lr)]
        count += 1
    return count


def is_done_part_2(positions):
    return all([position.endswith("Z") for _, position in positions.items()])


def do_part_2(processed_input):
    instructions, patterns, nodes = processed_input
    infinite_instructions = cycle(instructions)
    starts_nodes = [node for node in nodes if node.endswith("A")]

    positions = {node: node for node in starts_nodes}
    count = 0
    while not is_done_part_2(positions):
        lr = next(infinite_instructions)

        new_positions = {}
        for node, position in positions.items():
            new_positions[node] = patterns[(position, lr)]
        positions = new_positions
        count += 1
    return count


def do_visualization(processed_input):
    return None
