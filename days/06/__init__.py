from collections import deque
from itertools import islice

START_OF_PACKET_MARKER_LENGTH = 4
START_OF_MESSAGE_MARKER_LENGTH = 14

# Recipe from itertools https://docs.python.org/3/library/itertools.html
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        # First iteration
        yield tuple(window)
        # Because it is an iterator, we continue from where we left off below
    for x in it:
        # All other iterations
        window.append(x)
        yield tuple(window)


def get_end_of_marker_index(datastream, marker_length):
    for i, window in enumerate(sliding_window(datastream, marker_length)):
        if len(set(window)) == marker_length:
            return i + marker_length
    return "error"


def process_input(blob):
    return blob


def do_part_1(datastream):
    return get_end_of_marker_index(datastream, START_OF_PACKET_MARKER_LENGTH)


def do_part_2(datastream):
    return get_end_of_marker_index(datastream, START_OF_MESSAGE_MARKER_LENGTH)
