from year2019.intcode import IntCode


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
