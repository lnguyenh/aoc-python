from collections import defaultdict, deque

from utils.bfs import bfs


def bfs(edges, start, destination):
    # neighbours / graph
    neighbours = defaultdict(list)
    for from_node, to_node in edges:
        neighbours[from_node].append(to_node)

    visited = {start: True}

    q = deque([(start, 0)])

    while q:
        node, num_steps = q.popleft()

        for neighbour in neighbours[node]:
            if visited.get(neighbour):
                continue

            if neighbour == destination:
                return num_steps + 1

            q.append((neighbour, num_steps + 1))
            visited[node] = True

    return float("inf")


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
                    edges.append(((x, y), (x1, y1)))
    return edges, start, end, letters


def do_part_1(data):
    edges, start, end, _ = data
    cost = bfs(edges, start, end)
    return cost


def do_part_2(data):
    return
