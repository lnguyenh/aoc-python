from collections import deque

import math


# A function to perform division of
# large numbers
def longDivision(number, divisor):
    # As result can be very large
    # store it in string
    ans = ""

    # Find prefix of number that
    # is larger than divisor.
    idx = 0
    temp = ord(number[idx]) - ord("0")
    while temp < divisor:
        temp = temp * 10 + ord(number[idx + 1]) - ord("0")
        idx += 1

    idx += 1

    # Repeatedly divide divisor with temp.
    # After every division, update temp to
    # include one more digit.
    while (len(number)) > idx:
        # Store result in answer i.e. temp / divisor
        ans += chr(math.floor(temp // divisor) + ord("0"))

        # Take next digit of number
        temp = (temp % divisor) * 10 + ord(number[idx]) - ord("0")
        idx += 1

    ans += chr(math.floor(temp // divisor) + ord("0"))

    # If divisor is greater than number
    if len(ans) == 0:
        return "0"

    # else return ans
    return ans


class Transform:
    def __init__(self, operator, old_or_number):
        self.operator = operator
        if old_or_number == "old":
            self.is_self_referencing = True
            self.number = None
        else:
            self.is_self_referencing = False
            self.number = int(old_or_number)

    def do(self, x):
        if self.is_self_referencing:
            if self.operator == "*":
                return x * x
            elif self.operator == "+":
                return x + x
        else:
            if self.operator == "*":
                return x * self.number
            elif self.operator == "+":
                return x + self.number


class Monkey:
    def __init__(self, levels, transform, divisible, monkey_true, monkey_false):
        self.levels = deque(levels)
        self.transform = transform
        self.divisible = divisible
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.inspects = 0


class Game:
    def __init__(self, monkeys, do_divide):
        self.monkeys = monkeys
        self.monkey_ids = sorted([monkey_id for monkey_id, _ in monkeys.items()])
        self.do_divide = do_divide

    def play_one_round(self):
        for monkey_id in self.monkey_ids:
            monkey = self.monkeys[monkey_id]
            while monkey.levels:
                level = monkey.levels.popleft()
                new_level = monkey.transform.do(level)

                if self.do_divide:
                    new_level = int(new_level / 3)
                else:
                    pass
                if new_level % monkey.divisible == 0:
                    self.monkeys[monkey.monkey_true].levels.append(new_level)
                else:
                    self.monkeys[monkey.monkey_false].levels.append(new_level)
                monkey.inspects += 1

    def print(self, round_number):
        print(f"Round {round_number}:")
        for monkey_id in self.monkey_ids:
            print(f"{monkey_id}: {self.monkeys[monkey_id].levels}")
        print("\n")

    def play_n_rounds(self, n):
        for i in range(n):
            self.play_one_round()
            # self.print(i + 1)

    def multiply_top_two_inspects(self):
        inspects = sorted(
            [monkey.inspects for _, monkey in self.monkeys.items()], reverse=True
        )
        return inspects[0] * inspects[1]


def create_game(blob, do_divide):
    monkeys = {}
    raw_monkeys = blob.split("\n\n")
    for raw_monkey in raw_monkeys:
        lines = iter(raw_monkey.split("\n"))

        line = next(lines)
        monkey_id = line.replace(":", "").split(" ")[-1]

        line = next(lines)
        levels = [
            int(level)
            for level in line.replace("Starting items: ", "").strip().split(", ")
        ]
        line = next(lines)
        transform = Transform(
            *(line.replace("Operation: new = old ", "").strip().split(" "))
        )
        line = next(lines)
        divisible = int(line.split(" ")[-1])
        line = next(lines)
        monkey_true = line.split(" ")[-1]
        line = next(lines)
        monkey_false = line.split(" ")[-1]

        monkeys[monkey_id] = Monkey(
            levels, transform, divisible, monkey_true, monkey_false
        )
    return Game(monkeys, do_divide)


def process_input(blob):
    return blob


def do_part_1(blob):
    game = create_game(blob, do_divide=True)
    game.play_n_rounds(20)
    return game.multiply_top_two_inspects()


def do_part_2(blob):
    game = create_game(blob, do_divide=False)
    game.play_n_rounds(10000)
    return "toto"
