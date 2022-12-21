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
    monkeys = get_monkeys(blob)
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


def do_part_2(blob):
    # Create monkeys with the special setup for part 2
    monkeys = {}
    for line in blob.split("\n"):
        name, text = line.split(": ")
        monkeys[name] = text
    monkeys["humn"] = "X"
    monkeys["root"] = monkeys["root"].replace("+", "=")

    # Deal with the monkeys that already have a number from the get-go
    int_monkeys = {name: text for name, text in monkeys.items() if text.isnumeric()}
    for name in int_monkeys:
        monkeys.pop(name)
    for name, text in int_monkeys.items():
        for n in monkeys:
            monkeys[n] = monkeys[n].replace(name, text)

    # Replace strings when possible to get to a single equation with only one unknown
    while True:
        num_replaces = 0
        to_pop = []
        for n1 in monkeys:
            for n2 in monkeys:
                if n1 in monkeys[n2]:
                    monkeys[n2] = monkeys[n2].replace(n1, f"({monkeys[n1]})")
                    num_replaces += 1
            for name in to_pop:
                monkeys.pop(name)
        if num_replaces == 0:
            break

    print(monkeys["root"])

    return "Use the printed equation above in https://www.mathpapa.com/simplify-calculator/ to find the solution"
