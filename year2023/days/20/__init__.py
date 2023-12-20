from collections import namedtuple, defaultdict, deque

ON = "on"
OFF = "off"

LOW = "low"
HIGH = "high"

Pulse = namedtuple("Pulse", "origin receiver value")


class Module:
    def __init__(self, module_type, name, destinations):
        self.type = module_type
        self.name = name
        self.destinations = destinations
        self.state = OFF  # flip flops
        self.remembered = {}  # conjunctions
        self.origins = []

    def reset(self):
        self.state = OFF
        for origin in self.origins:
            self.remembered[origin] = LOW

    def toggle(self):
        if self.state == ON:
            self.state = OFF
        else:
            self.state = ON
        return self.state

    def remembered_only_highs(self):
        return all([r == HIGH for _, r in self.remembered.items()])


class Computer:
    def __init__(self, modules):
        self.modules = modules
        self.pulses = deque()
        self.counter = defaultdict(int)

    def apply_pulse(self, pulse, pulses, counters):
        doer = self.modules[pulse.receiver]

        if doer.type == "broadcaster":
            for d in doer.destinations:
                new_pulse = Pulse(pulse.receiver, d, pulse.value)
                pulses.append(new_pulse)
                counters[new_pulse.value] += 1
                # print(doer.name, "->", d, new_pulse.value)

        elif doer.type == "%":
            if pulse.value == LOW:
                state = doer.toggle()
                for d in doer.destinations:
                    new_pulse = Pulse(pulse.receiver, d, HIGH if state == ON else LOW)
                    pulses.append(new_pulse)
                    counters[new_pulse.value] += 1
                    # print(doer.name, "->", d, new_pulse.value)

        elif doer.type == "&":
            doer.remembered[pulse.origin] = pulse.value

            if doer.remembered_only_highs():
                for d in doer.destinations:
                    new_pulse = Pulse(pulse.receiver, d, LOW)
                    pulses.append(new_pulse)
                    counters[new_pulse.value] += 1
                    # print(doer.name, "->", d, new_pulse.value)
            else:
                for d in doer.destinations:
                    new_pulse = Pulse(pulse.receiver, d, HIGH)
                    pulses.append(new_pulse)
                    counters[new_pulse.value] += 1
                    # print(doer.name, "->", d, new_pulse.value)

        toto = 1

    def reset(self):
        for _, module in self.modules.items():
            module.reset()

    def process(self, initial_pulse):
        counters = defaultdict(int)
        for _ in range(1000):
            pulses = deque([initial_pulse])
            counters[initial_pulse.value] += 1
            while pulses:
                pulse = pulses.popleft()
                self.apply_pulse(pulse, pulses, counters)
        return counters[LOW] * counters[HIGH]


def process_input(blob):
    blob = blob.replace(" ->", "")
    blob = blob.replace(",", "")
    blob = blob.replace("broadcaster", "broadcaster broadcaster")
    blob = blob.replace("%", "% ")
    blob = blob.replace("&", "& ")
    lines = blob.split("\n")
    modules = {}
    for line in lines:
        module_type, name, destinations = line.split(" ", 2)
        destinations = destinations.split(" ")
        modules[name] = Module(module_type, name, destinations)

    # orphan modules
    for line in lines:
        module_type, name, destinations = line.split(" ", 2)
        destinations = destinations.split(" ")
        for d in destinations:
            if d not in modules:
                modules[d] = Module(d, d, [])

    for line in lines:
        module_type, name, destinations = line.split(" ", 2)
        destinations = destinations.split(" ")
        for d in destinations:
            modules[d].remembered[name] = LOW
            modules[d].origins.append(d)
    return modules


def do_part_1(modules):
    computer = Computer(modules)
    return computer.process(Pulse("button", "broadcaster", LOW))


def do_part_2(modules):
    return "toto"


def do_visualization(processed_input):
    return None
