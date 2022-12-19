def dfs(graph, source, visited, dfs_traversal):
    if source not in visited:
        dfs_traversal.append(source)
        visited.add(source)

        for neighbor_node in graph[source]:
            dfs(graph, neighbor_node, visited, dfs_traversal)

    return dfs_traversal


def main():
    visited = set()
    dfs_traversal = list()

    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F", "G"],
        "D": [],
        "E": [],
        "F": [],
        "G": [],
    }

    print(f"DFS: {dfs(graph, 'A', visited, dfs_traversal)}")


if __name__ == "__main__":
    main()
