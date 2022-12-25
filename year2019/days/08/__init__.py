def process_input(blob):
    return blob


def do_part_1(text):
    min_num_zeros = None
    result = None
    for chunk in zip(*(iter(text),) * (25 * 6)):
        num_zeros = chunk.count("0")
        num_ones = chunk.count("1")
        num_twos = chunk.count("2")
        if min_num_zeros is None or num_zeros < min_num_zeros:
            min_num_zeros = num_zeros
            result = num_ones * num_twos
    return result


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
