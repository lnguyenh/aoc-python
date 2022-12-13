def is_int_equal(a, b):
    return type(a) == int and type(b) == int and a == b


def is_in_right_order(left, right):
    # 2 ints
    if type(left) == int and type(right) == int:
        return left < right

    # Mixed
    if type(left) == int and type(right) == list:
        # left is int, right is list
        return is_in_right_order([left], right)
    if type(left) == list and type(right) == int:
        # left is list, right is int
        return is_in_right_order(left, [right])

    # 2 lists
    if type(left) == list and type(right) == list:
        max_length = max(len(left), len(right))
        max_l_i = len(left) - 1
        max_r_i = len(right) - 1

        # two empty lists
        if max_length == 0:
            return True

        # two lists
        for i in range(max_length):
            if i > max_l_i:
                # left runs out first
                return True
            if i > max_r_i:
                # right runs out first
                return False

            # equal
            if is_int_equal(left[i], right[i]):
                continue

            if is_in_right_order(left[i], right[i]):
                return True
            else:
                return False

        return True


def process_input(blob):
    pairs = []
    raw_pairs = blob.split("\n\n")
    for raw_pair in raw_pairs:
        line1, line2 = raw_pair.split("\n")
        a = eval(line1)
        b = eval(line2)
        pairs.append((a, b))
    return pairs


def do_part_1(pairs):
    count = 0
    index = 0
    result = 0
    for left, right in pairs:
        index += 1
        is_in_order = is_in_right_order(left, right)
        if is_in_order:
            count += 1
            result += index
            print(f"Pair {index} in order")
        else:
            print(f"Pair {index} NOT in order")
    return result


def do_part_2(processed_input):
    return "toto"
