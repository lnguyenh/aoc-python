from utils.grid import Grid
from year2019.intcode import IntCode


class Game(Grid):
    SKIP = (".",)

    def __init__(self, lines):
        super().__init__(lines)


def process_input(blob):
    return [int(n) for n in blob.split(",")]


def do_part_1(program):
    intcode = IntCode(
        program, seed=[0], silent=True, seed_only=True, pause_after_output=True
    )
    i = 0
    num_blocks = 0
    intcode.resume()
    while intcode.is_not_done:
        code = intcode.read()
        if i == 2:
            tile_id = code
            if tile_id == 2:
                num_blocks += 1
        i = (i + 1) % 3
        intcode.resume()
    return num_blocks


def do_part_2(program):
    return "toto"


def do_visualization(processed_input):
    return None
