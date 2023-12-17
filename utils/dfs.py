from collections import defaultdict, deque


def dfs(edges, start, destination):
    """
    Gets all paths between two nodes
    """

    # neighbours / graph
    neighbours = defaultdict(list)
    for from_node, to_node in edges:
        neighbours[from_node].append(to_node)

    # unique nodes
    nodes = set()
    for n1, n2 in edges:
        nodes.add(n1)
        nodes.add(n2)

    paths = deque([[start]])
    possible_paths = []

    if start == destination:
        return 0, [start]

    while paths:
        path = paths.pop()
        node = path[-1]

        # Getting the neighbours could be made dynamic for some aoc problems
        # based on problem rules instead of hardcoded list of edges
        for neighbour in neighbours[node]:
            new_path = list(path)
            new_path.append(neighbour)

            if neighbour == destination:
                possible_paths.append(new_path)

            paths.appendleft(new_path)  # that makes it a dfs?

    return possible_paths


if __name__ == "__main__":
    # Edges are directional
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "F"),
        ("C", "E"),
        ("C", "G"),
        ("G", "H"),
        ("E", "D"),
        ("C", "D"),
        ("H", "D"),
    ]
    print("A -> D:")
    print(dfs(edges, "A", "D"))
