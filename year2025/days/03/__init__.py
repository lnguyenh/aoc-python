def process_input(blob):
    x = blob.split("\n")
    result = []
    for line in x:
        result.append([y for y in line])
    return result


def do_part_1(processed_input):
    total = 0
    joltages = []
    for bank in processed_input:
        l = len(bank)
        first = max(bank[: l - 1])
        i_first = 0
        for i in range(l):
            if bank[i] == first:
                i_first = i
                break
        last = max(bank[i_first + 1 : l])
        number = int(str(first) + str(last))
        total += number
        joltages.append(number)
    return total


def get_number(bank, start_i, count, stack):

    end_i = len(bank) - count + 1
    x = max(bank[start_i:end_i])

    index = start_i
    for i in range(end_i - start_i):
        if bank[start_i + i] == x:
            index = start_i + i
            break
    stack.append(x)

    new_count = count - 1
    if new_count == 0:
        return stack

    return get_number(bank, index + 1, new_count, stack)


def do_part_2(processed_input):
    total = 0
    joltages = []
    for bank in processed_input:
        joltages.append(get_number(bank, 0, 12, []))

    human_joltages = []
    for i in joltages:
        number = int("".join([str(x) for x in i]))
        human_joltages.append(number)
        total += number
    return total


def do_visualization(processed_input):
    return None
