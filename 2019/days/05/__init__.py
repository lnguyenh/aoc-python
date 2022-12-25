from utils.regexp import search_groups


class IntCode:
    def __init__(self, program):
        self.p = program[:]
        self.original_program = program

    def parse_instruction(self, i):
        text = str(self.p[i]).rjust(5, "0")
        a, b, c, d = search_groups(r"(\d)?(\d)?(\d)?(\d?\d)$", text)
        return int(a), int(b), int(c), d

    def run_one(self, i):
        mode_1, mode_2, mode_3, code = self.parse_instruction(i)
        modes = mode_1, mode_2, mode_3
        instructions = {
            "01": self.add,
            "02": self.multiply,
            "03": self.input,
            "04": self.output,
            "99": self.finish,
        }
        return instructions[code](i, modes)

    def get_value(self, i, mode):
        content = self.p[i]
        return content if mode else self.p[content]

    def add(self, i, modes):
        a = self.get_value((i + 1), modes[2])
        b = self.get_value((i + 2), modes[1])
        total = a + b
        c = self.p[i + 3]
        self.p[c] = total
        return i + 4

    def multiply(self, i, modes):
        a = self.get_value(i + 1, modes[2])
        b = self.get_value(i + 2, modes[1])
        total = a * b
        c = self.p[i + 3]
        self.p[c] = total
        return i + 4

    def input(self, i, modes):
        print("Type input value:")
        value = input()
        a = self.p[i + 1]
        self.p[a] = int(value)
        return i + 2

    def output(self, i, modes):
        if modes[2]:
            print(f"{self.p[1 + 1]}")
        else:
            a = self.p[i + 1]
            print(f"{self.p[a]}")
        return i + 2

    def finish(self, i, modes):
        return None

    def run(self):
        i = 0
        while True:
            i = self.run_one(i)
            if i is None:
                break

    def set(self, value, index):
        self.p[index] = value

    def reset(self):
        self.p = self.original_program[:]


def process_input(blob):
    return [int(n) for n in blob.split(",")]


def do_part_1(program):
    intcode = IntCode(program)
    intcode.run()
    return "toto"


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
