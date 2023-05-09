from collections import namedtuple
from math import floor

from utils.grid import Point


State = namedtuple("State", "profile instruction_index shape_index")
Step = namedtuple("Step", "block_number height")


class Tetris:
    def __init__(self, instruction):
        self.instructions = instruction
        self.current_instruction = 0

        self.shapes = ["-", "+", "l", "i", "o"]
        self.current_shape = 0

        self.height = 0

        self.profile = {
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        }

        self.states = {}

    def save_new_profile(self, block):
        old_height = max([y for x, y in self.profile if x == 1])

        # Add block to profile
        for p, value in block.items():
            self.profile.add((p.x, p.y))

        # Save new height
        new_height = max([y for x, y in self.profile if x == 1])

        # Generate new profile
        new_profile = set()
        x = 1
        y = new_height + 1

        delta_height = new_height - old_height
        direction = "right"

        while True:
            if x == 8:
                break

            down = (x, y - 1)
            right = (x + 1, y)
            up = (x, y + 1)
            left = (x - 1, y)

            if direction == "right":
                if down in self.profile:
                    new_profile.add(down)
                else:
                    x, y = down
                    direction = "down"
                    continue
                if right in self.profile:
                    new_profile.add(right)
                else:
                    x, y = right
                    direction = "right"
                    continue
                direction = "up"
                continue
            elif direction == "down":
                if left in self.profile:
                    new_profile.add(left)
                else:
                    x, y = left
                    direction = "left"
                    continue
                if down in self.profile:
                    new_profile.add(down)
                else:
                    x, y = down
                    direction = "down"
                    continue
                direction = "right"
                continue
            elif direction == "left":
                if up in self.profile:
                    new_profile.add(up)
                else:
                    x, y = up
                    direction = "up"
                    continue
                if left in self.profile:
                    new_profile.add(left)
                else:
                    x, y = left
                    direction = "left"
                    continue
                direction = "down"
                continue
            elif direction == "up":
                if right in self.profile:
                    new_profile.add(right)
                else:
                    x, y = right
                    direction = "right"
                    continue
                if up in self.profile:
                    new_profile.add(up)
                else:
                    x, y = up
                    direction = "up"
                    continue
                direction = "left"
                continue

        self.height = self.height + delta_height
        new_profile = set([(x, y - delta_height) for x, y in new_profile])
        self.profile = new_profile

    def skip(self, state, current_step, end_block_number):
        old_step = self.states[state]
        print(f"found {state}: {old_step}")

        # Fastforward to last bit after all the repetitions
        times = int(
            floor(
                (end_block_number - old_step.block_number)
                / (current_step.block_number - old_step.block_number)
            )
        )
        self.height = old_step.height + times * (self.height - old_step.height)
        num_blocks_remaining = (end_block_number - old_step.block_number) % (
            current_step.block_number - old_step.block_number
        )
        return num_blocks_remaining

    def create_new_shape(self):
        shape = self.shapes[self.current_shape]
        self.current_shape += 1
        self.current_shape = self.current_shape % (len(self.shapes))

        block = {}
        ref_y = self.highest_y + 4  # first y of the new shape

        if shape == "-":
            block[Point(3, ref_y)] = "-"
            block[Point(4, ref_y)] = "-"
            block[Point(5, ref_y)] = "-"
            block[Point(6, ref_y)] = "-"
        elif shape == "+":
            block[Point(4, ref_y)] = "+"
            block[Point(3, ref_y + 1)] = "+"
            block[Point(4, ref_y + 1)] = "+"
            block[Point(5, ref_y + 1)] = "+"
            block[Point(4, ref_y + 2)] = "+"
        elif shape == "l":
            block[Point(3, ref_y)] = "l"
            block[Point(4, ref_y)] = "l"
            block[Point(5, ref_y)] = "l"
            block[Point(5, ref_y + 1)] = "l"
            block[Point(5, ref_y + 2)] = "l"
        elif shape == "i":
            block[Point(3, ref_y)] = "i"
            block[Point(3, ref_y + 1)] = "i"
            block[Point(3, ref_y + 2)] = "i"
            block[Point(3, ref_y + 3)] = "i"
        elif shape == "o":
            block[Point(3, ref_y)] = "o"
            block[Point(4, ref_y)] = "o"
            block[Point(3, ref_y + 1)] = "o"
            block[Point(4, ref_y + 1)] = "o"
        return block

    def block_touches_ground(self, block):
        for b_point in block:
            for x, y in self.profile:
                if b_point.x == x:
                    if b_point.y == y + 1:
                        return True
        return False

    def block_touches_left(self, block):
        if any([p.x == 1 for p in block]):
            return True
        for bp in block:
            for x, y in self.profile:
                if bp.y == y and bp.x == x + 1:
                    return True
        return False

    def block_touches_right(self, block):
        if any([p.x == 7 for p in block]):
            return True
        for bp in block:
            for x, y in self.profile:
                if bp.y == y and bp.x == x - 1:
                    return True
        return False

    @property
    def highest_y(self):
        return max([y for _, y in self.profile])

    def run(self, end_block_number):
        for i in range(end_block_number):
            block = self.create_new_shape()

            # self.print(block)
            while True:
                block = self.do_horizontal(block)
                # self.print(block)
                if self.block_touches_ground(block):
                    # self.print(block)
                    self.save_new_profile(block)
                    break
                block = self.move_down(block)
                # self.print(block)

    def run_with_loop_finding(self, end_block_number):
        block_number = 0
        while True:
            block_number += 1
            block = self.create_new_shape()

            # self.print(block)
            while True:
                block = self.do_horizontal(block)
                # self.print(block)
                if self.block_touches_ground(block):
                    self.save_new_profile(block)

                    state = State(
                        tuple(self.profile),
                        self.current_instruction,
                        self.current_shape,
                    )
                    step = Step(block_number, self.height)

                    if state in self.states:
                        remaining_blocks = self.skip(state, step, end_block_number)
                        return self.run(remaining_blocks)
                    else:
                        self.states[state] = step
                    break
                block = self.move_down(block)
                # self.print(block)

    def do_horizontal(self, block):
        instruction = self.instructions[self.current_instruction]
        if instruction == ">":
            if not self.block_touches_right(block):
                block = self.move_right(block)
        elif instruction == "<":
            if not self.block_touches_left(block):
                block = self.move_left(block)
        self.current_instruction += 1
        self.current_instruction = self.current_instruction % len(self.instructions)
        return block

    def move_right(self, block):
        return {Point(p.x + 1, p.y): value for p, value in block.items()}

    def move_left(self, block):
        return {Point(p.x - 1, p.y): value for p, value in block.items()}

    def move_down(self, block):
        return {Point(p.x, p.y - 1): value for p, value in block.items()}

    def print(self, block):
        max_y = max([p.y for p in block])
        min_y = min([y for _, y in self.profile])
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(1, 8):
                b = block.get(Point(x, y))
                if (x, y) in self.profile:
                    line += "#"
                elif b:
                    line += b
                else:
                    line += "."
            print(line)
        print("\n")


def process_input(blob):
    return [c for c in blob]


def do_part_1(jets):
    tetris = Tetris(jets)
    tetris.run(end_block_number=2022)
    return tetris.highest_y + tetris.height


def do_part_2(jets):
    tetris = Tetris(jets)
    tetris.run_with_loop_finding(end_block_number=1000000000000)
    return tetris.highest_y + tetris.height
