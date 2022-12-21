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


def process_input(blob):
    lines = blob.split("\n")
    monkeys = {}
    for line in lines:
        name, text = line.split(": ")
        monkeys[name] = Monkey(name, text)
    return monkeys


def do_part_1(monkeys):
    while monkeys["root"].number is None:
        for name, m in monkeys.items():
            if not m.number:
                if not m.av:
                    m.av = monkeys.get(m.a).number
                if not m.bv:
                    m.bv = monkeys.get(m.b).number
            if m.can_solve():
                m.solve()
    return int(monkeys["root"].number)


def do_part_2(monkeys):
    return "toto"
