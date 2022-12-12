from collections import defaultdict
from heapq import heappop, heappush


# https://gist.github.com/kachayev/5990802
def djikstra(edges, start, destination):
    # edges are tuples: (start-node-name, end-node-name, cost)
    nodes = defaultdict(list)
    for from_node, to_node, cost in edges:
        nodes[from_node].append((cost, to_node))

    q = [(0, start, ())]
    seen = set()
    mins = {start: 0}  # maintains shortest cost to all the nodes

    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path += (v1,)
            if v1 == destination:
                return cost, path

            for cost_v1_to_v2, v2 in nodes.get(v1, ()):
                # loop through all the v2s that can bet attained from v1
                if v2 in seen:  # v2 has already be dealt with as a v1
                    continue
                current_min_total_cost_to_v2 = mins.get(v2, None)
                candidate_total_cost_to_v2 = cost + cost_v1_to_v2
                if (
                    current_min_total_cost_to_v2 is None
                    or candidate_total_cost_to_v2 < current_min_total_cost_to_v2
                ):
                    mins[v2] = candidate_total_cost_to_v2  # update total min cost to v2
                    heappush(q, (candidate_total_cost_to_v2, v2, path))

    return float("inf"), None


if __name__ == "__main__":
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11),
    ]

    print("=== Dijkstra ===")
    print(edges)
    print("A -> E:")
    print(djikstra(edges, "A", "E"))
    print("F -> G:")
    print(djikstra(edges, "F", "G"))
