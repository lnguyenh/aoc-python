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

    def best_next_valve(self, minutes, valve_names, valves):
        worth = {}
        for destination in valve_names:
            if destination == self.name:
                continue
            if valves[destination].is_open:
                continue
            minutes_to_reach = len(self.shortest_paths[destination]) - 1
            minutes_left = minutes - minutes_to_reach - 1
            if minutes_left <= 0:
                continue
            value = valves[destination].rate * minutes_left
            worth[destination] = value, minutes_left

        if not worth:
            return None

        max_destination = None
        for destination, data in worth.items():
            if not max_destination:
                max_destination = destination
            elif worth[destination][0] > worth[max_destination][0]:
                max_destination = destination

        return max_destination, worth[max_destination][0], worth[max_destination][1]

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


def calculate_flow(path, num_steps, valves):
    is_open = {valve_name: False for valve_name in valves}
    total_pressure = 0
    pressure_step = 0

    i = 0
    num_minutes = 0
    while num_steps > 0:
        # Update pressure
        total_pressure += pressure_step
        num_steps -= 1
        num_minutes += 1
        if num_steps == 0:
            break

        if i >= len(path):
            continue

        valve_name = path[i]

        if not is_open[valve_name] and valves[valve_name].rate > 0:
            is_open[valve_name] = True
            pressure_step += valves[valve_name].rate
        else:
            i += 1

        if i >= len(path):
            next_valve = valve_name
        else:
            next_valve = path[i]
        toto = 3
    return total_pressure, pressure_step


def get_best_reward(
    minutes_left, valve_name, all_names, visited, reward, possible_rewards
):
    if minutes_left < 0:
        return []
    if valve_name not in visited:
        reward += possible_rewards[valve_name]
        visited.add(valve_name)
    remaining_names = all_names - visited
    for name in remaining_names:
        pass


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
        for to_valve_name in p[1:]:
            to_valve = valves[to_valve_name]

            minutes_needed = len(from_valve.shortest_paths[to_valve_name]) - 1
            if minutes + minutes_needed > 30:
                break

            minutes += minutes_needed + 1
            minutes_left = 30 - minutes
            candidate_total += minutes_left * to_valve.rate
            from_valve = to_valve
        if candidate_total > total:
            total = candidate_total
    return total

    total = 0
    from_valve = valves["AA"]
    for p in permutations(valve_names_2):
        candidate_total = 0
        minutes = 0
        for to_valve_name in p:
            to_valve = valves[to_valve_name]

            minutes_needed = len(from_valve.shortest_paths[to_valve_name]) - 1
            if minutes + minutes_needed > 30:
                break

            minutes += minutes_needed + 1
            minutes_left = 30 - minutes
            candidate_total += minutes_left * to_valve.rate
            from_valve = to_valve
        if candidate_total > total:
            total = candidate_total

    return total

    current_valve = "AA"
    total = 0
    minutes = 30
    while current_valve:
        results = valves[current_valve].best_next_valve(minutes, valve_names, valves)
        if results is None:
            current_valve = None
            continue
        next_valve, value, minutes_left = results
        current_valve = next_valve
        valves[current_valve].is_open = True
        total += value
        minutes = minutes_left

    return total


def do_part_2(processed_input):
    return "toto"
