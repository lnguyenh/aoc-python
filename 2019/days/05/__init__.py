class IntCode:
    def __init__(self, program):
        self.p = program[:]
        self.original_program = program

    def run_one(self, i):
        instr = self.p[i]

        if instr == 1:
            a, b, c = self.p[i + 1], self.p[i + 2], self.p[i + 3]
            self.p[c] = self.p[a] + self.p[b]
            return i + 4
        elif instr == 2:
            a, b, c = self.p[i + 1], self.p[i + 2], self.p[i + 3]
            self.p[c] = self.p[a] * self.p[b]
            return i + 4
        elif instr == 3:
            a = self.p[i + 1]
            print("Type input value:")
            value = input()
            self.p[a] = value
            return i + 2
        elif instr == 4:
            print(f"{self.p[a]}")
            return i + 2
        elif instr == 99:
            return None

    def run(self):
        i = 0
        while True:
            i = self.run_one(i)
            if i is None:
                break

    def get_value(self, index):
        return self.p[index]

    def set(self, value, index):
        self.p[index] = value

    def reset(self):
        self.p = self.original_program[:]


def process_input(blob):
    return blob.split("\n")


def do_part_1(processed_input):
    return "toto"


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
