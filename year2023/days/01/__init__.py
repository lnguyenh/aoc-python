AS_LETTERS = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}


def process_input(blob):
    lines = blob.split("\n")
    digits_1 = [[c for c in line if c.isdigit()] for line in lines]

    lines_2 = []
    for line in lines:
        for as_string, as_number in AS_LETTERS.items():
            line = line.replace(as_string, as_number)
        lines_2.append(line)
    digits_2 = [[c for c in line if c.isdigit()] for line in lines_2]

    return (
        [int(digit[0] + digit[-1]) for digit in digits_1],
        [int(digit[0] + digit[-1]) for digit in digits_2],
    )


def do_part_1(processed_input):
    numbers, _ = processed_input
    return sum(numbers)


def do_part_2(processed_input):
    _, numbers = processed_input
    return sum(numbers)


def do_visualization(processed_input):
    return None
