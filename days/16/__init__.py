import itertools
from collections import defaultdict

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

    @property
    def num_useful_valves(self):
        return len(self.shortest_paths_useful.keys())

    def get_paths(self, minutes, valves, visited):
        if self.num_useful_valves - len(visited) == 0 or minutes >= 30:
            return [[self.name]]

        paths = []
        new_visited = set(list(visited))
        new_visited.add(self.name)

        for valve_name, path in self.shortest_paths_useful.items():
            if valve_name not in new_visited:
                to_valve = valves[valve_name]
                new_minutes = minutes + (len(path) + 1)
                for p in to_valve.get_paths(new_minutes, valves, new_visited):
                    paths.append([self.name] + p)
        return paths

    def get_paths_2(self, minutes, valves, visited, whitelist):
        if len(whitelist) - len(visited) == 0 or minutes >= 26:
            return [[self.name]]

        paths = []
        new_visited = set(list(visited))
        new_visited.add(self.name)

        for valve_name in whitelist:
            if valve_name not in new_visited:
                path = self.shortest_paths_useful[valve_name]
                to_valve = valves[valve_name]
                new_minutes = minutes + (len(path) + 1)
                for p in to_valve.get_paths_2(
                    new_minutes, valves, new_visited, whitelist
                ):
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
    return None
    rates, edges, valves = data
    valve_names = valves.keys()
    for _, valve in valves.items():
        valve.compute_shortest_paths(valve_names, edges)
        valve.populate_useful(valves)

    from_valve = valves["AA"]
    visited = set()
    paths = from_valve.get_paths(0, valves, visited)
    total = 0

    for p in paths:
        candidate_total = 0
        minutes = 0
        real_path = p[1:]
        from_valve = valves["AA"]
        for to_valve_name in real_path:
            to_valve = valves[to_valve_name]

            minutes_needed = len(from_valve.shortest_paths_useful[to_valve_name]) + 1
            if minutes + minutes_needed >= 30:
                break

            minutes += minutes_needed
            minutes_left = 30 - minutes
            candidate_total += minutes_left * to_valve.rate
            from_valve = to_valve
        if candidate_total > total:
            total = candidate_total
    return total


def two_partitions(S):
    res_list = []
    for l in range(0, int(len(S) / 2) + 1):
        combis = set(itertools.combinations(S, l))
        for c in combis:
            res_list.append((sorted(list(c)), sorted(list(S - set(c)))))
    return res_list


def do_part_2(data):
    rates, edges, valves = data
    valve_names = valves.keys()
    for _, valve in valves.items():
        valve.compute_shortest_paths(valve_names, edges)
        valve.populate_useful(valves)
    useful_valve_names = [name for name, valve in valves.items() if valve.rate > 0]

    partitions = two_partitions(set(useful_valve_names))

    aa_valve = valves["AA"]
    visited = set()
    combos = []
    for whitelist1, whitelist2 in partitions:
        if len(whitelist1) < 6 or len(whitelist2) < 6:
            continue
        paths1 = aa_valve.get_paths_2(0, valves, visited, whitelist1)
        paths2 = aa_valve.get_paths_2(0, valves, visited, whitelist2)
        for p1 in paths1:
            for p2 in paths2:
                combos.append((p1, p2))

    z = (["AA", "DD", "HH", "EE"], ["AA", "JJ", "BB", "CC"]) in combos

    total = 0
    for combo in combos:
        candidate_total = 0
        for p in combo:
            minutes = 0
            real_path = p[1:]
            from_valve = valves["AA"]
            for to_valve_name in real_path:
                to_valve = valves[to_valve_name]

                minutes_needed = (
                    len(from_valve.shortest_paths_useful[to_valve_name]) + 1
                )
                if minutes + minutes_needed >= 26:
                    break

                minutes += minutes_needed
                minutes_left = 26 - minutes
                candidate_total += minutes_left * to_valve.rate
                from_valve = to_valve
        if candidate_total > total:
            total = candidate_total

    return total
