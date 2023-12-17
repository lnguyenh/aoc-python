from collections import deque


def process_input(blob):
    return blob.split("\n")[0]


def reacts(c1, c2):
    return abs(ord(c1) - ord(c2)) == 32


def do_part_1(line):
    q = deque()
    for c in line:
        prev_c = q.pop() if q else None
        if prev_c is None:
            q.append(c)
        elif not reacts(prev_c, c):
            q.extend([prev_c, c])
    return len(q)


def do_part_2(line):
    results = []
    for x in range(65, 91):
        q = deque()
        ords_to_skip = [x, x + 32]
        for c in line:
            if ord(c) in ords_to_skip:
                continue
            prev_c = q.pop() if q else None
            if prev_c is None:
                q.append(c)
            elif not reacts(prev_c, c):
                q.extend([prev_c, c])
        results.append(len(q))
    return min(results)


def do_visualization(processed_input):
    return None
