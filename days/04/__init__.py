def process_input(blob):
    return [
        [[int(a) for a in x.split("-")] for x in line.split(",")]
        for line in blob.split("\n")
    ]


def is_in(a, b):
    return a[0] <= b[0] and a[1] >= b[1] or a[1] <= b[1] and a[0] >= b[0]


def has_overlap(zone1_start, zone1_end, zone2_start, zone2_end):
    return bool(
        set(range(zone1_start, zone1_end + 1)).intersection(
            range(zone2_start, zone2_end + 1)
        )
    )


def do_part_1(pairs):
    return sum([1 for pair in pairs if is_in(pair[0], pair[1])])


def do_part_2(pairs):
    return sum([1 for zone1, zone2 in pairs if has_overlap(*zone1, *zone2)])
