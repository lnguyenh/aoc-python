from collections import deque, OrderedDict

TEST_START = {
    "1": "ZN",
    "2": "MCD",
    "3": "P",
}

START = {
    "1": "RNPG",
    "2": "TJBLCSVH",
    "3": "TDBMNL",
    "4": "RVPSB",
    "5": "GCQSWMVH",
    "6": "WQSCDBJ",
    "7": "FQL",
    "8": "WMHTDLFV",
    "9": "LPBVMJF",
}


class Stacker:
    def __init__(self, stacks, moves):
        self.original_stacks = stacks
        self.stacks = OrderedDict()
        self.reset_stacks()
        self.moves = moves

    def reset_stacks(self):
        self.stacks = OrderedDict()
        for name, packets in self.original_stacks.items():
            self.stacks[name] = deque(packets)

    def process_9000(self):
        for n, origin, destination in self.moves:
            for _ in range(int(n)):
                self.stacks[destination].append(self.stacks[origin].pop())

    def process_9001(self):
        for n, origin, destination in self.moves:
            block = deque()
            for _ in range(int(n)):
                block.append(self.stacks[origin].pop())
            for _ in range(int(n)):
                self.stacks[destination].append(block.pop())

    def get_last_word(self):
        return "".join([stack.pop() for _, stack in self.stacks.items()])


def process_input(blob):
    stacks, moves = blob.split("\n\n")
    num_stacks = int(stacks.split("\n")[-1].split(" ")[-1])
    moves = moves.replace("move ", "").replace(" from ", ",").replace(" to ", ",")
    moves = [line.split(",") for line in moves.split("\n")]
    stacker = Stacker(START if num_stacks > 5 else TEST_START, moves)
    return stacker


def do_part_1(stacker):
    stacker.process_9000()
    return stacker.get_last_word()


def do_part_2(stacker):
    stacker.reset_stacks()
    stacker.process_9001()
    return stacker.get_last_word()
