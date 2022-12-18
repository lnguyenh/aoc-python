from collections import defaultdict


def process_input(blob):
    lines = blob.split("\n")
    coordinates = []
    for line in lines:
        x, y, z = line.split(",")
        coordinates.append((int(x), int(y), int(z)))
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
        xs[(y, z)].append(x)

    for x, y, z in coordinates:
        ys[(z, x)].append(y)

    for x, y, z in coordinates:
        zs[(x, y)].append(z)

    for key in xs:
        xs[key] = sorted(xs[key])

    for key in ys:
        ys[key] = sorted(ys[key])

    for key in zs:
        zs[key] = sorted(zs[key])

    total = sum([count_axis(xs), count_axis(ys), count_axis(zs)])
    return total


def get_bubble(bubble, coordinates, checked, xmin, xmax, ymin, ymax, zmin, zmax):
    could_expand = False
    new_bubble = bubble.copy()
    for x, y, z in bubble - checked:
        expansions = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y - 1, z),
            (x, y + 1, z),
            (x, y, z - 1),
            (x, y, z + 1),
        ]
        for x1, y1, z1 in expansions:
            if not (
                xmin - 1 <= x1 <= xmax + 1
                and ymin - 1 <= y1 <= ymax + 1
                and zmin - 1 <= z1 <= zmax + 1
            ):
                # out of bound. This is not a bubble
                return None
            if (x1, y1, z1) in coordinates:
                # cannot expand here, there is a cube
                continue
            new_bubble.add((x1, y1, z1))
            could_expand = True
    if could_expand:
        return get_bubble(
            new_bubble, coordinates, bubble, xmin, xmax, ymin, ymax, zmin, zmax
        )
    else:
        return bubble


def do_part_2(coordinates):
    x_list = [x for x, _, _ in coordinates]
    y_list = [y for _, y, _ in coordinates]
    z_list = [z for _, _, z in coordinates]
    xmin = min(x_list)
    ymin = min(y_list)
    zmin = min(z_list)
    xmax = max(x_list)
    ymax = max(y_list)
    zmax = max(z_list)

    points_to_check = set()
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                if (x, y, z) not in coordinates:
                    points_to_check.add((x, y, z))

    bubbles = set()
    for x, y, z in points_to_check:
        if any([(x, y, z) in b for b in bubbles]):
            continue
        bubble = get_bubble(
            {(x, y, z)}, coordinates, set(), xmin, xmax, ymin, ymax, zmin, zmax
        )
        if bubble:
            bubbles.add(frozenset(bubble))

    for bubble in bubbles:
        for x, y, z in bubble:
            coordinates.append((x, y, z))

    return do_part_1(coordinates)
