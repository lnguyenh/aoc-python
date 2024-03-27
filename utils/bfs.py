from collections import defaultdict, deque


def bfs(edges, start, destination):
    """
    Gets shortest path from start to destination using BFS
    Good for graphs when cost between nodes is always equal
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

    # visited marker
    visited = {node: False for node in nodes}

    visited[start] = True
    paths = deque([[start]])

    if start == destination:
        return 0, [start]

    while paths:
        path = paths.popleft()
        node = path[-1]

        # Getting the neighbours could be made dynamic for some aoc problems
        # based on problem rules instead of hardcoded list of edges
        for neighbour in neighbours[node]:
            if visited[neighbour]:
                continue
            new_path = list(path)
            new_path.append(neighbour)

            if neighbour == destination:
                return len(new_path), new_path

            paths.append(new_path)
            visited[node] = True

    return float("inf"), None


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
    ]
    print("A -> D:")
    print(bfs(edges, "A", "D"))
