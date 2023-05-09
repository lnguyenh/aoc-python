def process_input(blob):
    return blob.split("\n")


def do_part_1(changes):
    return sum([int(x) for x in changes])


def do_part_2(changes):
    frequencies = set()
    frequency = 0
    index = -1
    num_changes = len(changes)
    while True:
        if frequency in frequencies:
            break
        frequencies.add(frequency)
        index = (index + 1) % num_changes
        frequency += int(changes[index])

    return frequency


def do_visualization(processed_input):
    return None
