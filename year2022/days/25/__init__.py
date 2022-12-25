from collections import deque

NORMAL_DIGIT = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
SAFU_DIGIT = {"2": "2", "1": "1", "0": "0", "-1": "-", "-2": "="}


def add_safus(safus):
    counters = [0] * 20
    for safu in safus:
        for i, x in enumerate(safu[::-1]):
            counters[i] += NORMAL_DIGIT[x]
    return counters


def simplify_safu(digits):
    for i in range(len(digits) - 1):
        if digits[i] > 0:
            x = digits[i] // 5
            r = digits[i] % 5
            digits[i + 1] += x
            digits[i] = r
            if r == 3:
                digits[i + 1] += 1
                digits[i] = -2
            if r == 4:
                digits[i + 1] += 1
                digits[i] = -1

        elif digits[i] < 0:
            x = -digits[i] // 5
            r = -digits[i] % 5
            digits[i + 1] -= x
            digits[i] = -r
            if r == 3:
                digits[i + 1] -= 1
                digits[i] = 2
            if r == 4:
                digits[i + 1] -= 1
                digits[i] = 1
    return digits


def process_input(blob):
    return blob.split("\n")


def do_part_1(safus):
    blob = add_safus(safus)
    simplified = deque(simplify_safu(blob)[::-1])
    while simplified[0] == 0:
        # remove extra zeros
        simplified.pop()
    new_safu = [SAFU_DIGIT[str(x)] for x in simplified]
    return "".join(new_safu)


def do_part_2(processed_input):
    return "toto"
