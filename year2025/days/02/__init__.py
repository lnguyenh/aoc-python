def process_input(blob):
    line = blob.split("\n")[0]
    raw_ranges = line.split(",")
    ranges = []
    for r in raw_ranges:
        start, end = r.split("-")
        ranges.append((int(start), int(end)))
    return ranges


def is_valid_1(s):
    l = len(s)
    if l % 2 != 0:
        return True
    a = 0
    b = l // 2 - 1
    c = l // 2
    d = l - 1

    w1 = s[a : b + 1]
    w2 = s[c : d + 1]
    if w1 == w2:
        # print(f"Found repeat: {w1} at {a}-{b} and {c}-{d} for {s}")
        return False
    return True


def is_valid_2(s):
    l = len(s)
    multiplier = 2
    while True:
        window_size = l // multiplier
        if window_size == 0:
            break
        if window_size * multiplier > l:
            break
        if l % multiplier != 0:
            multiplier += 1
            continue
        # print("Checking", s, multiplier)
        words = []
        start = 0
        for m in range(multiplier):
            a = start
            b = start + window_size
            words.append(s[a:b])
            start += window_size
        # print(words)

        if len(set(words)) == 1:
            # print(f"Found repeat: {words} for {s}")
            return False

        multiplier += 1

    return True


def do_part_1(processed_input):
    total = 0
    for start, stop in processed_input:
        # print("processing range", start, stop)
        for x in range(start, stop + 1):
            s = str(x)
            if not is_valid_1(s):
                total += x
    return total


def do_part_2(processed_input):
    total = 0
    for start, stop in processed_input:
        # print("processing range", start, stop)
        for x in range(start, stop + 1):
            s = str(x)
            if not is_valid_2(s):
                total += x
    return total


def do_visualization(processed_input):
    return None
