import operator
from collections import namedtuple, defaultdict, deque

OPERATORS = {
    "<": operator.lt,
    ">": operator.gt,
}
INVERT = {operator.lt: operator.ge, operator.gt: operator.le}


Rule = namedtuple("Rule", "m0 operator m1 destination")
Condition = namedtuple("Condition", "m0 operator m1")


class Workflow:
    def __init__(self, instructions):
        self.instructions = self.extract_instructions(instructions)

    def extract_instructions(self, instructions):
        parsed_instructions = []
        for instr in instructions.split(","):
            if ":" in instr:
                m = instr[0]
                o = OPERATORS[instr[1]]
                v, d = instr[2:].split(":")
                parsed_instructions.append(Rule(m, o, int(v), d))
            else:
                parsed_instructions.append(Rule(None, None, None, instr))
        return parsed_instructions

    def process(self, part):
        for rule in self.instructions:
            if not rule.operator:
                return rule.destination
            if rule.operator(part[rule.m0], rule.m1):
                return rule.destination
        else:
            raise Exception


def process_input(blob):
    blob = blob.replace("}", "")
    ws, ps = blob.split("\n\n")
    workflows = {}
    for w in ws.split("\n"):
        name, instructions = w.split("{")
        workflows[name] = Workflow(instructions)
    parts = []
    ps_ = ps.replace("x=", "")
    ps_ = ps_.replace("m=", "")
    ps_ = ps_.replace("a=", "")
    ps_ = ps_.replace("s=", "")
    ps_ = ps_.replace("{", "")
    ps_ = ps_.replace("}", "")
    for p in ps_.split("\n"):
        x, m, a, s = p.split(",")
        parts.append({"x": int(x), "m": int(m), "a": int(a), "s": int(s)})
    return workflows, parts


def do_part_1(processed_input):
    workflows, parts = processed_input
    accepted = []
    rejected = []
    for part in parts:
        workflow_name = "in"
        while True:
            destination = workflows[workflow_name].process(part)
            if destination == "A":
                accepted.append(part)
                break
            elif destination == "R":
                rejected.append(part)
                break
            workflow_name = destination
    values = []
    for part in accepted:
        part_values = [v for k, v in part.items()]
        values += part_values
    return sum(values)


def do_part_2(processed_input):
    workflows, _ = processed_input
    conditions = {}
    edges = []
    for w, workflow in workflows.items():
        for i, rule in enumerate(workflow.instructions):
            if rule.operator:
                cs = [
                    Condition(r.m0, INVERT[r.operator], r.m1)
                    for r in workflow.instructions[:i]
                ] + [Condition(rule.m0, rule.operator, rule.m1)]
                conditions[(w, i)] = (
                    cs,
                    w,
                    rule.destination,
                )
            else:
                cs = [
                    Condition(r.m0, INVERT[r.operator], r.m1)
                    for r in workflow.instructions[:-1]
                ]
                conditions[(w, i)] = (
                    cs,
                    w,
                    rule.destination,
                )  # conditions ,origin, destination

    for key, (_, w_from, w_to) in conditions.items():
        edges.append((w_from, w_to, key))

    # neighbours / graph
    neighbours = defaultdict(list)
    for from_node, to_node, rule_key in edges:
        neighbours[from_node].append((to_node, rule_key))

    # unique nodes
    nodes = set()
    for n1, n2, _ in edges:
        nodes.add(n1)
        nodes.add(n2)

    paths = deque([[("in", "")]])
    destination = "A"
    possible_paths = []

    while paths:
        path = paths.pop()
        node, rule = path[-1]

        # Getting the neighbours could be made dynamic for some aoc problems
        # based on problem rules instead of hardcoded list of edges
        for neighbour in neighbours[node]:
            new_path = list(path)
            new_path.append(neighbour)

            if neighbour[0] == destination:
                possible_paths.append(new_path)

            paths.appendleft(new_path)  # that makes it a dfs?

    all_path_conditions = []
    for path in possible_paths:
        path_conditions = []
        for node, key in path:
            if key:
                path_conditions.append(key)
        cs = []
        for key in path_conditions:
            cs.extend(conditions[key][0])
        all_path_conditions.append(cs)

    results = 0
    for pcs in all_path_conditions:
        xs_ = []
        ms_ = []
        as_ = []
        ss_ = []
        for x in range(1, 4001):
            for c in pcs:
                if c.m0 == "x":
                    if c.operator(x, c.m1):
                        xs_.append(x)
        for m in range(1, 4001):
            for c in pcs:
                if c.m0 == "m":
                    if c.operator(m, c.m1):
                        ms_.append(m)
        for a in range(1, 4001):
            for c in pcs:
                if c.m0 == "a":
                    if c.operator(a, c.m1):
                        as_.append(a)
        for s in range(1, 4001):
            for c in pcs:
                if c.m0 == "s":
                    if c.operator(s, c.m1):
                        ss_.append(s)
        results += len(as_) * len(xs_) * len(ms_) * len(ss_)

    return results


def do_visualization(processed_input):
    return None


# 167409079868000
# 48976201428000
