def process_input(blob):
    return blob.split("\n")


def do_part_1(processed_input):
    position = 50
    count = 0
    for line in processed_input:
        direction = line[0]
        steps = int(line[1:])

        if direction == "R":
            position += steps
        elif direction == "L":
            position -= steps
        else:
            raise ValueError(f"Unknown direction: {direction}")

        position = position % 100
        if position == 0:
            count += 1

    return count


def do_part_2(processed_input):
    position = 50
    count = 0
    for line in processed_input:
        direction = line[0]
        steps = int(line[1:])

        for _ in range(steps):
            if direction == "L":
                position = position - 1
            elif direction == "R":
                position = position + 1
            else:
                raise ValueError(f"Unknown direction: {direction}")
            position = position % 100
            if position == 0:
                count += 1
    return count


def do_visualization(processed_input):
    return None
