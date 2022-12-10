def process_input(blob):
    lines = blob.replace("addx", "").replace("noop", "").split("\n")
    delta = []
    current_x = 1
    x = []
    for i, line in enumerate(lines):
        if not line:
            delta.append(0)
            x.append(current_x)
            continue

        dx = int(line)

        delta.append(0)
        x.append(current_x)

        delta.append(dx)
        current_x += dx
        x.append(current_x)
    return x


def do_part_1(x):
    return (
        20 * x[18]
        + 60 * x[58]
        + 100 * x[98]
        + 140 * x[138]
        + 180 * x[178]
        + 220 * x[218]
    )


def do_part_2(x):
    line = ""
    for i in range(len(x)):
        if i == 0:
            sprite = [0, 1, 2]
        else:
            sprite = [x[i - 1], x[i - 1] + 1, x[i - 1] - 1]

        if i % 40 in sprite:
            line += "#"
        else:
            line += "."
        if (i + 1) % 40 == 0:
            print(line)
            line = ""

    return "Read the image above in the terminal"
