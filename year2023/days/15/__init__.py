from collections import OrderedDict
from functools import lru_cache


def process_input(blob):
    return blob.split(",")


@lru_cache
def get_hash(word):
    cv = 0
    for c in word:
        cv += ord(c)
        cv *= 17
        cv = cv % 256
    return cv


def do_part_1(processed_input):
    hashes = []
    for word in processed_input:
        hashes.append(get_hash(word))
    return sum(hashes)


def do_part_2(processed_input):

    boxes = []
    for _ in range(256):
        boxes.append(OrderedDict())

    for word in processed_input:
        if word.endswith("-"):
            label = word[:-1]
            h = get_hash(label)
            boxes[h].pop(label, None)
        else:
            label, n = word.split("=")
            h = get_hash(label)
            boxes[h][label] = n

    focus_powers = []
    for i, box in enumerate(boxes, start=1):
        for position, label in enumerate(box.keys(), start=1):
            focus_powers.append(i * position * int(box[label]))

    return sum(focus_powers)
