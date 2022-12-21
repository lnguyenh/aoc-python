from math import floor


class Monkey:
    def __init__(self, name, text):
        self.name = name
        self.number = None
        self.a = None
        self.av = None
        self.b = None
        self.bv = None
        self.o = None

        elements = text.split(" ")
        if len(elements) == 1:
            self.number = int(elements[0])
        else:
            self.a, self.o, self.b = elements

    def can_solve(self):
        return self.av is not None and self.bv is not None

    def solve(self):
        if self.o == "+":
            self.number = self.av + self.bv
        elif self.o == "*":
            self.number = self.av * self.bv
        elif self.o == "/":
            self.number = self.av / self.bv
        elif self.o == "-":
            self.number = self.av - self.bv
        return self.number


def process_input(blob):
    return blob


def get_monkeys(blob, humn=None):
    lines = blob.split("\n")
    monkeys = {}
    for line in lines:
        name, text = line.split(": ")
        monkeys[name] = Monkey(name, text)
    if humn is not None:
        monkeys["humn"].number = humn

    return monkeys


def do_part_1(blob):
    return None
    # monkeys = get_monkeys(blob)
    # while monkeys["root"].number is None:
    #     for name, m in monkeys.items():
    #         if not m.number:
    #             if not m.av:
    #                 m.av = monkeys.get(m.a).number
    #             if not m.bv:
    #                 m.bv = monkeys.get(m.b).number
    #         if m.can_solve():
    #             m.solve()
    # return int(monkeys["root"].number)


def do_part_2(blob):
    i = 0
    while True:
        monkeys = get_monkeys(blob, humn=i)
        abort = False
        while not monkeys["root"].can_solve() and not abort:
            for name, m in monkeys.items():
                if m.number is None:
                    if not m.av:
                        m.av = monkeys.get(m.a).number
                    if not m.bv:
                        m.bv = monkeys.get(m.b).number
                if m.can_solve():
                    r = m.solve()
                    if floor(r) != r:
                        abort = True
                        break
        if monkeys["root"].can_solve() and monkeys["root"].av == monkeys["root"].bv:
            break
        i += 1

    return i
