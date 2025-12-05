from itertools import combinations


def process_input(blob):
    range_blob, ingredient_blob = blob.split("\n\n")
    ranges = set()
    for line in range_blob.split("\n"):
        start, stop = line.split("-")
        ranges.add((int(start), int(stop)))
    ingredients = [int(i) for i in ingredient_blob.split("\n")]
    return ranges, ingredients


def do_part_1(processed_input):
    ranges, ingredients = processed_input
    count = 0
    for i in ingredients:
        for r in ranges:
            if r[0] <= i <= r[1]:
                count += 1
                break
    return count


def do_part_2(processed_input):
    ranges, _ = processed_input

    while True:
        merge_done = False
        for r0, r1 in combinations(ranges, 2):
            if r0[0] <= r1[0] <= r0[1] <= r1[1]:
                ranges.remove(r0)
                ranges.remove(r1)
                ranges.add((r0[0], r1[1]))
                merge_done = True
                break
            elif r1[0] <= r0[0] <= r1[1] <= r0[1]:
                ranges.remove(r0)
                ranges.remove(r1)
                ranges.add((r1[0], r0[1]))
                merge_done = True
                break
            elif r1[0] <= r0[0] <= r0[1] <= r1[1]:
                ranges.remove(r0)
                ranges.remove(r1)
                ranges.add((r1[0], r1[1]))
                merge_done = True
                break
            elif r0[0] <= r1[0] <= r1[1] <= r0[1]:
                ranges.remove(r0)
                ranges.remove(r1)
                ranges.add((r0[0], r0[1]))
                merge_done = True
                break
        if not merge_done:
            break

    count = 0
    for start, stop in ranges:
        count += stop - start + 1

    return count


def do_visualization(processed_input):
    return None
