import operator
from collections import namedtuple


OPERATORS = {
    "<": operator.lt,
    ">": operator.gt,
}


Rule = namedtuple("Rule", "m0 operator m1 destination")


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
    return "toto"


def do_visualization(processed_input):
    return None
