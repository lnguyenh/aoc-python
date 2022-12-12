from utils.djikstra import djikstra
from utils.grid import get_name, name_to_xy


def process_input(blob):
    edges = []
    letters = {}
    start = None
    end = None
    for y, line in enumerate(blob.split("\n")):
        for x, letter in enumerate(line):
            if letter == "S":
                start = get_name(x, y)
                letters[get_name(x, y)] = "a"
            elif letter == "E":
                end = get_name(x, y)
                letters[get_name(x, y)] = "z"
            else:
                letters[get_name(x, y)] = letter
    for key, letter in letters.items():
        x, y = name_to_xy(key)
        for x1, y1 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            adjacent_letter = letters.get(get_name(x1, y1))
            if adjacent_letter:
                delta = ord(adjacent_letter) - ord(letter)
                if delta <= 1:
                    edges.append((get_name(x, y), get_name(x1, y1), 1))
    return edges, start, end, letters


def do_part_1(data):
    edges, start, end, _ = data
    cost, _ = djikstra(edges, start, end)
    return cost


def do_part_2(data):
    shortest = None
    edges, start, end, letters = data
    for key, letter in letters.items():
        if letter == "a":
            cost, _ = djikstra(edges, key, end)
            if not shortest:
                shortest = cost
            else:
                shortest = min(shortest, cost)
    return shortest
