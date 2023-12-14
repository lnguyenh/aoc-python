from collections import defaultdict, Counter


def process_input(blob):
    blob = blob.replace(" Guard #", "")
    blob = blob.replace(" begins shift", "")
    blob = blob.replace(" asleep", "")
    blob = blob.replace(" up", "")
    blob = blob.replace(" falls", "zfalls")
    blob = blob.replace(" wakes", "zwakes")
    blob = blob.replace(" ", "x")
    blob = blob.replace("[", "")
    blob = blob.replace("]", " ")
    blob = blob.replace("z", "")
    lines = blob.split("\n")

    entries = []
    for line in lines:
        entries.append(line.split(" "))
    entries = sorted(entries, key=lambda x: x[0])

    guard = None
    start = None

    time_slept = defaultdict(int)
    minutes_slept = defaultdict(list)

    for timestamp, v in entries:
        if v.isdigit():
            guard = v
        elif v == "falls":
            start = int(timestamp.split(":")[1])
        elif v == "wakes":
            stop = int(timestamp.split(":")[1])
            time_slept[guard] += stop - start
            for i in range(start, stop):
                minutes_slept[guard].append(i)

    return time_slept, minutes_slept


def do_part_1(processed_input):
    time_slept, minutes_slept = processed_input

    sleepy_guard = None
    max_slept = 0
    for guard, slept_time in time_slept.items():
        if not sleepy_guard or slept_time > max_slept:
            sleepy_guard = guard
            max_slept = slept_time

    minute_counts = Counter(minutes_slept[sleepy_guard])
    minute_counts = sorted(
        list(minute_counts.items()), key=lambda x: x[1], reverse=True
    )

    return minute_counts[0][0] * int(sleepy_guard)


def do_part_2(processed_input):
    _, minutes_slept = processed_input

    minute_records = {}
    for guard, min_slept in minutes_slept.items():
        minute_counts = Counter(minutes_slept[guard])
        for minute, count in minute_counts.items():
            if minute not in minute_records or minute_records[minute][1] < count:
                minute_records[minute] = (guard, count)

    minute_records = sorted(
        list(minute_records.items()), key=lambda x: x[1][1], reverse=True
    )

    return minute_records[0][0] * int(minute_records[0][1][0])
