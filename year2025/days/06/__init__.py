import operator

from utils.grid import Grid

OP_MAP = {
    "+": operator.add,
    "*": operator.mul,
}


class Table(Grid):
    def __init__(self, lines):
        super().__init__(lines)

    def number(self, x):
        n_str = ""
        for y in range(self.maxy + 1):
            c = self.grid.get((x, y))
            if c and c.isdigit():
                n_str += c
        if len(n_str):
            return int(n_str)
        return None


def process_input(blob):
    lines = blob.split("\n")
    values = []
    for line in lines:
        v = line.split(" ")
        clean_row = [x for x in v if x != ""]
        values.append(clean_row)
    l = len(values)
    return values[: l - 1], values[l - 1], lines


def do_part_1(processed_input):
    rows, operators, _ = processed_input
    result = 0
    for i in range(len(operators)):
        total = 0
        for j in range(len(rows)):
            if j == 0:
                total = int(rows[j][i])
                continue
            num = int(rows[j][i])
            op = operators[i]
            total = OP_MAP[op](total, num)
        result += total
    return result


def do_part_2(processed_input):
    rows, operators, lines = processed_input
    table = Table(lines)
    result = 0
    op = None
    total = 0
    for x in range(table.maxx + 1):
        if (
            table.grid.get((x, table.maxy))
            and table.grid.get((x, table.maxy)) != ""
            and table.grid.get((x, table.maxy)) != " "
        ):
            op = table.grid.get((x, table.maxy))
            total = 0

        if n := table.number(x):
            if total == 0:
                total = n
            else:
                total = OP_MAP[op](total, n)
        else:
            result += total
            total = 0
    result += total
    return result


def do_visualization(processed_input):
    return None
