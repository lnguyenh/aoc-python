from collections import namedtuple

from utils.strings import remove_from_string

Mapping = namedtuple("Mapping", "source_min source_max destination_min")


def process_input(blob):
    conversions = blob.split("\n\n")
    seeds_string = remove_from_string(conversions[0], ["seeds: "])
    seeds = [int(number) for number in seeds_string.split(" ")]

    hops = []
    for block in conversions[1:]:
        lines = block.split("\n")
        mappings = []
        for line in lines[1:]:
            mappings.append([int(number) for number in line.split(" ")])
        friendly_mappings = []
        for destination, source, length in mappings:
            source_min = source
            source_max = source + length - 1
            destination_min = destination
            friendly_mappings.append(Mapping(source_min, source_max, destination_min))
        hops.append(friendly_mappings)

    return seeds, hops


def do_part_1(processed_input):
    seeds, hops = processed_input
    min_location = None
    for seed in seeds:
        position = seed

        # Each step
        for mappings in hops:

            # Each possible mapping
            for mapping in mappings:
                if mapping.source_min <= position <= mapping.source_max:
                    new_position = mapping.destination_min + (
                        position - mapping.source_min
                    )
                    position = new_position
                    break
            else:
                # explicit
                position = position

        if min_location is None or position < min_location:
            min_location = position

    return min_location


def do_one_hop(intervals, hop):
    output = set()
    pending = set()

    if not intervals:
        return output

    for start, stop in intervals:
        for mapping in hop:

            # interval fully contained
            if mapping.source_min <= start and stop <= mapping.source_max:
                output.add(
                    (
                        mapping.destination_min + start - mapping.source_min,
                        mapping.destination_min + stop - mapping.source_min,
                    )
                )
                break

            # start is inside
            if mapping.source_min <= start <= mapping.source_max < stop:
                output.add(
                    (
                        mapping.destination_min + start - mapping.source_min,
                        mapping.destination_min
                        + mapping.source_max
                        - mapping.source_min,
                    )
                )
                pending.add((mapping.source_max + 1, stop))
                break

            # stop is inside
            if start < mapping.source_min <= stop <= mapping.source_max:
                output.add(
                    (
                        mapping.destination_min,
                        mapping.destination_min + stop - mapping.source_min,
                    )
                )
                pending.add((start, mapping.source_min - 1))
                break
        else:
            output.add((start, stop))

    return output | do_one_hop(pending, hop)


def do_part_2(processed_input):
    seeds, hops = processed_input
    intervals = []
    for seed_start, length in zip(*(iter(seeds),) * 2):
        intervals.append((seed_start, seed_start + length - 1))
    intervals = set(intervals)
    for hop in hops:
        intervals = do_one_hop(intervals, hop)

    return min([start for start, _ in intervals])
