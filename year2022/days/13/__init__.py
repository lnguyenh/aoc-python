def is_int_equal(a, b):
    # Gotcha: 2 is equal to [[2]]
    while True:
        if type(a) == int and type(b) == int:
            return a == b
        if type(a) == list:
            if len(a) != 1:
                return False
            a = a[0]
        if type(b) == list:
            if len(b) != 1:
                return False
            b = b[0]


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
            # print(f"Pair {index} in order")
        else:
            pass
            # print(f"Pair {index} NOT in order")
    return result


def do_part_2(pairs):
    packets = []
    for left, right in pairs:
        packets.append(left)
        packets.append(right)
    packets.append([[2]])
    packets.append([[6]])
    num_switches = 1
    while num_switches:
        num_switches = 0
        for i in range(len(packets) - 1):
            if not is_in_right_order(packets[i], packets[i + 1]):
                x = packets[i + 1]
                packets[i + 1] = packets[i]
                packets[i] = x
                num_switches += 1
    a = None
    b = None
    for i, p in enumerate(packets):
        if p == [[2]]:
            a = i + 1
        if p == [[6]]:
            b = i + 1
    return a * b
