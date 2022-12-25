from collections import deque
from utils.regexp import search_groups


class IntCode:
    def __init__(self, program, seed=None, silent=False, seed_only=False):
        self.p = program[:]
        self.original_program = program[:]
        self.seed = deque(seed) if seed else deque([])
        self.silent = silent
        self.last_output = None
        self.seed_only = seed_only
        self.i = 0
        self.done = False

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
        if self.seed:
            value = self.seed.popleft()
            # print(f"Using seed input value: {value}")
        elif self.seed_only:
            self.pause(i)
            return None
        elif not self.seed_only:
            print("Type input value:")
            value = input()
        a = self.p[i + 1]
        self.p[a] = int(value)
        return i + 2

    def _output(self, i, modes):
        if modes[2]:
            result = self.p[1 + 1]
        else:
            a = self.p[i + 1]
            result = self.p[a]
        if self.silent:
            self.last_output = result
        else:
            print(f"Output is: {result}")
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

    def run(self, from_i=0):
        i = from_i
        while True:
            i = self.run_one(i)
            if i is None:
                if self.i is None:
                    self.done = True
                break

    def pause(self, i):
        self.i = i

    def resume(self):
        if not self.done:
            i = self.i
            self.i = None
            self.run(i)

    def set(self, value, index):
        self.p[index] = value

    def add_to_seed(self, value):
        self.seed.append(value)

    def reset(self):
        self.p = self.original_program[:]

    def read(self):
        last_output = self.last_output
        self.last_output = None
        return last_output
