from itertools import permutations

from utils.djikstra import djikstra


class Valve:
    def __init__(self, name, rate, to_valves):
        self.name = name
        self.rate = int(rate)
        self.to_valves = to_valves
        self.is_open = False
        self.shortest_paths = {}
        self.shortest_paths_useful = {}

    def compute_shortest_paths(self, valve_names, edges):
        for destination in valve_names:
            self.shortest_paths[destination] = djikstra(edges, self.name, destination)[
                1
            ]

    def populate_useful(self, valves):
        for valve_name, path in self.shortest_paths.items():
            if valves[valve_name].rate > 0:
                self.shortest_paths_useful[valve_name] = path[1:]

    def get_paths(self, minutes_left, valves, visited):
        if (
            len(self.shortest_paths_useful.keys()) - len(visited) == 0
            or minutes_left < 0
        ):
            return [[self.name]]

        paths = []
        new_visited = set(list(visited))
        new_visited.add(self.name)

        for valve_name, path in self.shortest_paths_useful.items():
            if valve_name not in new_visited:
                to_valve = valves[valve_name]
                new_minutes_left = minutes_left - (len(path) + 1)
                for p in to_valve.get_paths(new_minutes_left, valves, new_visited):
                    paths.append([self.name] + p)
        return paths


def process_input(blob):
    lines = (
        blob.replace("Valve ", "")
        .replace(" has flow rate=", ";")
        .replace(" tunnels lead to valves ", "")
        .replace(" tunnel leads to valve ", "")
        .replace(" ", "")
        .split("\n")
    )
    rates = {}
    edges = []
    valves = {}
    for line in lines:
        name, rate, raw_valves = line.split(";")
        rates[name] = rate
        to_valves = raw_valves.split(",")
        for valve in to_valves:
            edges.append((name, valve, 1))
        valves[name] = Valve(name, rate, to_valves)
    return rates, edges, valves


def do_part_1(data):
    rates, edges, valves = data
    valve_names = valves.keys()
    for _, valve in valves.items():
        valve.compute_shortest_paths(valve_names, edges)
        valve.populate_useful(valves)

    edges_2 = []
    for origin, valve in valves.items():
        for destination, path in valve.shortest_paths.items():
            if valves[destination].rate > 0 and origin != destination:
                edges_2.append((origin, destination, len(path)))
    valve_names_2 = [name for name, valve in valves.items() if valve.rate > 0]

    from_valve = valves["AA"]
    visited = set()
    paths = from_valve.get_paths(30, valves, visited)
    total = 0
    from_valve = valves["AA"]
    for p in paths:
        candidate_total = 0
        minutes = 0
        real_path = p[1:]
        for to_valve_name in real_path:
            to_valve = valves[to_valve_name]

            minutes_needed = len(from_valve.shortest_paths_useful[to_valve_name]) + 1
            if minutes + minutes_needed > 30:
                break

            minutes += minutes_needed
            minutes_left = 30 - minutes
            candidate_total += minutes_left * to_valve.rate
            from_valve = to_valve
        if candidate_total > total:
            total = candidate_total
    return total


def do_part_2(processed_input):
    return "toto"
