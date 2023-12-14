from collections import defaultdict


def process_input(blob):
    blob = blob.replace(":", "")
    blob = blob.replace("#", "")
    blob = blob.replace("@ ", "")
    blob = blob.replace("x", " ")
    blob = blob.replace(",", " ")

    final_lines = []
    for line in blob.split("\n"):
        [a, b, c, d, e] = line.split(" ")
        final_lines.append((int(a), int(b), int(c), int(d), int(e)))
    grid = defaultdict(list)
    for [n, x, y, w, h] in final_lines:
        for i in range(x, x + w):
            for j in range(y, y + h):
                grid[(i, j)].append(n)
    return grid, final_lines


def do_part_1(processed_input):
    grid, _ = processed_input
    crowded_xys = [k for k in grid.keys() if len(grid[k]) > 1]
    return len(crowded_xys)


def do_part_2(processed_input):
    grid, final_lines = processed_input
    for [n, x, y, w, h] in final_lines:
        is_good = True
        for i in range(x, x + w):
            for j in range(y, y + h):
                if len(grid[(i, j)]) > 1:
                    is_good = False
                    break
            if not is_good:
                break
        else:
            return n
    return None
