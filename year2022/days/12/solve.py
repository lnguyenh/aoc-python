from collections import defaultdict, deque


def bfs(edges, start, destination):
    return 0


def process_input(blob):
    edges = []
    letters = {}
    start = None
    end = None

    # Model the grid as a dictionary
    # The key is the position as a tuple (x, y). the value is the letter at that position
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

    # Build the graph edges
    for key, letter in letters.items():
        x, y = key
        for x1, y1 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            adjacent_letter = letters.get((x1, y1))
            if adjacent_letter:
                delta = ord(adjacent_letter) - ord(letter)
                if delta <= 1:
                    edges.append(((x, y), (x1, y1)))

    return edges, start, end, letters


def do_part_1(data):
    edges, start, end, _ = data
    cost = bfs(edges, start, end)
    return cost


def do_part_2(data):
    return


if __name__ == "__main__":
    # Edges are directional
    test_edges = [
        ("A", "B"),
        ("A", "X"),
        ("B", "C"),
        ("B", "Y"),
        ("C", "F"),
        ("C", "E"),
        ("C", "G"),
        ("G", "H"),
        ("E", "D"),
        ("C", "D"),
    ]
    print("A -> D:")
    print(bfs(test_edges, "A", "D"))
    print("the answer should be 3")
