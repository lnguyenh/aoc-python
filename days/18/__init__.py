from collections import defaultdict


def process_input(blob):
    lines = blob.split("\n")
    coordinates = []
    for line in lines:
        x, y, z = line.split(",")
        coordinates.append((x, y, z))
    return coordinates


def num_adjacents(l):
    count = 0
    if len(l) == 1:
        return 0
    for i in range(len(l) - 1):
        if l[i + 1] - l[i] == 1:
            count += 1
    return count


def count_axis(axis):
    count = 0
    for _, l in axis.items():
        count = count + 2 * len(l) - 2 * num_adjacents(l)
    return count


def do_part_1(coordinates):
    xs = defaultdict(list)
    ys = defaultdict(list)
    zs = defaultdict(list)

    for x, y, z in coordinates:
        xs[(y, z)].append(int(x))

    for x, y, z in coordinates:
        ys[(z, x)].append(int(y))

    for x, y, z in coordinates:
        zs[(x, y)].append(int(z))

    for key in xs:
        xs[key] = sorted(xs[key])

    for key in ys:
        ys[key] = sorted(ys[key])

    for key in zs:
        zs[key] = sorted(zs[key])

    total = sum([count_axis(xs), count_axis(ys), count_axis(zs)])
    return total


def do_part_2(processed_input):
    return "toto"
