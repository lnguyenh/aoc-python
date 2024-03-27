from utils.djikstra import djikstra


def process_input(blob):
    edges = []
    letters = {}
    start = None
    end = None
    for y, line in enumerate(blob.split("\n")):
        for x, letter in enumerate(line):
            if letter == "S":
                start = (x, y)
                letters[(x, y)] = "a"
            elif letter == "E":
                end = (x, y)
                letters[(x, y)] = "z"
            else:
                letters[(x, y)] = letter
    for key, letter in letters.items():
        x, y = key
        for x1, y1 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            adjacent_letter = letters.get((x1, y1))
            if adjacent_letter:
                delta = ord(adjacent_letter) - ord(letter)
                if delta <= 1:
                    edges.append(((x, y), (x1, y1), 1))
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
