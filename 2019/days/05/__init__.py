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
            "01": self._add,
            "02": self._multiply,
            "03": self._input,
            "04": self._output,
            "05": self._jump_if_true,
            "06": self._jump_if_false,
            "07": self._less_than,
            "08": self._equals,
            "99": self._finish,
        }
        return instructions[code](i, modes)

    def get_value(self, i, mode):
        content = self.p[i]
        return content if mode else self.p[content]

    def get_two_params(self, i, modes):
        a = self.get_value((i + 1), modes[2])
        b = self.get_value((i + 2), modes[1])
        return a, b

    def get_three_params(self, i, modes):
        a = self.get_value((i + 1), modes[2])
        b = self.get_value((i + 2), modes[1])
        c = self.p[i + 3]
        return a, b, c

    def _add(self, i, modes):
        a, b, c = self.get_three_params(i, modes)
        self.p[c] = a + b
        return i + 4

    def _multiply(self, i, modes):
        a, b, c = self.get_three_params(i, modes)
        self.p[c] = a * b
        return i + 4

    def _input(self, i, modes):
        print("Type input value:")
        value = input()
        a = self.p[i + 1]
        self.p[a] = int(value)
        return i + 2

    def _output(self, i, modes):
        if modes[2]:
            print(f"{self.p[1 + 1]}")
        else:
            a = self.p[i + 1]
            print(f"{self.p[a]}")
        return i + 2

    def _jump_if_true(self, i, modes):
        a, b = self.get_two_params(i, modes)
        if a != 0:
            return b
        else:
            return i + 3

    def _jump_if_false(self, i, modes):
        a, b = self.get_two_params(i, modes)
        if a == 0:
            return b
        else:
            return i + 3

    def _less_than(self, i, modes):
        a, b, c = self.get_three_params(i, modes)
        self.p[c] = 1 if a < b else 0
        return i + 4

    def _equals(self, i, modes):
        a, b, c = self.get_three_params(i, modes)
        self.p[c] = 1 if a == b else 0
        return i + 4

    def _finish(self, i, modes):
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
