from utils.djikstra import djikstra


class Valve:
    def __init__(self, name, rate, to_valves):
        self.name = name
        self.rate = int(rate)
        self.to_valves = to_valves
        self.is_open = False
        self.shortest_paths = {}

    def compute_shortest_paths(self, valve_names, edges):
        for destination in valve_names:
            self.shortest_paths[destination] = djikstra(edges, self.name, destination)[
                1
            ]

    def best_next_valve(self, minutes, valve_names, valves):
        worth = {}
        for destination in valve_names:
            if valves[destination].is_open:
                continue
            minutes_to_reach = len(self.shortest_paths[destination])
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

    def get_paths(self, num, valves):
        if num == 1:
            a = [[self.name]]
            return a

        paths = []
        for to_valve in self.to_valves:
            valve = valves[to_valve]
            for path in valve.get_paths(num - 1, valves):
                a = [self.name]
                paths.append(a + path)
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

    current_valve = "AA"
    total = 0
    minutes = 30
    while current_valve:
        results = valves[current_valve].best_next_valve(minutes, valve_names, valves)
        if results is None:
            current_valve = None
            continue
        next_valve, value, minutes_left = results
        total += value
        minutes = minutes_left

    return total


def do_part_2(processed_input):
    return "toto"
