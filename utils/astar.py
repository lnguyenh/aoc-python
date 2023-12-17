from collections import defaultdict
from heapq import heappop, heappush


def manhattan_fn(from_point, to_point):
    x0, y0 = from_point
    x1, y1 = to_point
    return abs(x1 - x0) + abs(y1 - y0)  # manhattan distance


def astar(edges, start, destination, heuristic_fn=manhattan_fn):
    """
    Gets shortest path from start to destination using Astar
    Good for graphs when cost between nodes is not equal
    """
    # edges are tuples: (start-node-name, end-node-name, cost)
    nodes = defaultdict(list)
    for from_node, to_node, cost in edges:
        nodes[from_node].append((cost, to_node))

    q = [(0, 0, start, ())]  # (astar_cost, node, path)
    seen = set()
    mins = {start: 0}  # maintains shortest cost to all the nodes

    while q:
        (astar_cost_to_v1, cost_to_v1, v1, path) = heappop(q)

        if v1 not in seen:
            # At each iteration we only process the first element of the heap
            # This means the next unseen point which is closest from our start node
            # Put a breakpoint line 17 and run this file to understand if needed

            seen.add(v1)
            path += (v1,)
            if v1 == destination:
                return cost_to_v1, path

            for cost_v1_to_v2, v2 in nodes.get(v1, ()):
                # loop through all the v2s that can bet attained from v1
                if v2 in seen:  # v2 has already be dealt with as a v1
                    continue
                current_min_cost_to_v2 = mins.get(v2, None)
                candidate_cost_to_v2 = cost_to_v1 + cost_v1_to_v2
                candidate_astar_cost_to_v2 = candidate_cost_to_v2 + heuristic_fn(v1, v2)
                if (
                    current_min_cost_to_v2 is None
                    or candidate_cost_to_v2 < current_min_cost_to_v2
                ):
                    # We found a new total min cost to v2
                    mins[v2] = candidate_cost_to_v2  # update total min cost to v2
                    heappush(
                        q,
                        (
                            candidate_astar_cost_to_v2,
                            candidate_cost_to_v2,
                            v2,
                            path,
                        ),
                    )

    return float("inf"), None


if __name__ == "__main__":
    problem_edges = [
        ((0, 0), (0, 1), 1),
        ((0, 0), (0, 2), 99),
        ((0, 1), (0, 3), 2),
        ((0, 1), (0, 2), 3),
    ]
    print("(0, 0) -> (0, 2):")
    print(astar(problem_edges, (0, 1), (0, 2), manhattan_fn))
