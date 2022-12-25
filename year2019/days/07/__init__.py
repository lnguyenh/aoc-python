from itertools import permutations

from year2019.intcode import IntCode


def process_input(blob):
    return [int(n) for n in blob.split(",")]


def run_thruster(program, a, b, c, d, e):
    intcode1 = IntCode(program, [a, 0], silent=True)
    intcode1.run()
    intcode2 = IntCode(program, [b, intcode1.last_output], silent=True)
    intcode2.run()
    intcode3 = IntCode(program, [c, intcode2.last_output], silent=True)
    intcode3.run()
    intcode4 = IntCode(program, [d, intcode3.last_output], silent=True)
    intcode4.run()
    intcode5 = IntCode(program, [e, intcode4.last_output], silent=True)
    intcode5.run()

    return intcode5.last_output


def run_thruster2(program, a, b, c, d, e):
    signal = 0
    intcode_a = IntCode(program, [a], silent=True, seed_only=True)
    intcode_b = IntCode(program, [b], silent=True, seed_only=True)
    intcode_c = IntCode(program, [c], silent=True, seed_only=True)
    intcode_d = IntCode(program, [d], silent=True, seed_only=True)
    intcode_e = IntCode(program, [e], silent=True, seed_only=True)

    while True:
        if signal is not None:
            intcode_a.add_to_seed(signal)
        intcode_a.resume()
        to_b = intcode_a.read()

        if to_b is not None:
            intcode_b.add_to_seed(to_b)
        intcode_b.resume()
        to_c = intcode_b.read()

        if to_c is not None:
            intcode_c.add_to_seed(to_c)
        intcode_c.resume()
        to_d = intcode_c.read()

        if to_d is not None:
            intcode_d.add_to_seed(to_d)
        intcode_d.resume()
        to_e = intcode_d.read()

        if to_e is not None:
            intcode_e.add_to_seed(to_e)
        intcode_e.resume()
        signal = intcode_e.read()

        if all(
            [
                intcode.done
                for intcode in [intcode_a, intcode_b, intcode_c, intcode_d, intcode_e]
            ]
        ):
            break

    return signal


def do_part_1(program):
    highest_signal = None
    for a, b, c, d, e in permutations([0, 1, 2, 3, 4]):
        result = run_thruster(program, a, b, c, d, e)
        if highest_signal is None or result > highest_signal:
            highest_signal = result
    return highest_signal


def do_part_2(program):
    highest_signal = None
    for a, b, c, d, e in permutations([5, 6, 7, 8, 9]):
        result = run_thruster2(program, a, b, c, d, e)
        if highest_signal is None or result > highest_signal:
            highest_signal = result
    return highest_signal


def do_visualization(processed_input):
    return None
