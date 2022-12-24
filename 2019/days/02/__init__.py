class IntCode:
    def __init__(self, program):
        self.p = program[:]
        self.original_program = program

    def run_one(self, i):
        instr = self.p[i]
        a, b, c = self.p[i + 1], self.p[i + 2], self.p[i + 3]
        if instr == 1:
            self.p[c] = self.p[a] + self.p[b]
            return i + 4
        elif instr == 2:
            self.p[c] = self.p[a] * self.p[b]
            return i + 4
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
    return [int(n) for n in blob.split(",")]


def do_part_1(processed_input):
    intcode = IntCode(processed_input)
    if len(processed_input) > 30:
        # real problem, not example
        intcode.set(12, 1)
        intcode.set(2, 2)
    intcode.run()
    return intcode.get_value(0)


def do_part_2(processed_input):
    intcode = IntCode(processed_input)
    for noun in range(100):
        for verb in range(100):
            intcode.reset()
            intcode.set(noun, 1)
            intcode.set(verb, 2)
            intcode.run()
            if intcode.get_value(0) == 19690720:
                return 100 * noun + verb


def do_visualization(processed_input):
    return None
