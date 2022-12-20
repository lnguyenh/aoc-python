class Node:
    def __init__(self, number, i):
        self.i = i
        self.value = number
        self.n = None
        self.p = None

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"


def process_input(blob):
    nodes = [Node(int(x), i) for i, x in enumerate(blob.split("\n"))]
    for i, node in enumerate(nodes):
        if i == 0:
            node.p = len(nodes) - 1
            node.n = i + 1
        elif i == len(nodes) - 1:
            node.n = 0
            node.p = i - 1
        else:
            node.n = i + 1
            node.p = i - 1
    return nodes


def find_target(node, nodes):
    steps = node.value
    target_node = node
    if steps > 0:
        for _ in range(steps):
            target_node = nodes[target_node.n]
            if target_node.i == node.i:
                target_node = nodes[target_node.n]
    if steps < 0:
        for _ in range(-steps + 1):
            target_node = nodes[target_node.p]
            if target_node.i == node.i:
                target_node = nodes[target_node.p]
    return target_node


def unlink_node(node, nodes):
    previous_node = nodes[node.p]
    next_node = nodes[node.n]
    previous_node.n = next_node.i
    next_node.p = previous_node.i
    return node


def print_nodes(nodes):
    current_node = None
    for node in nodes:
        if node.value == 0:
            current_node = node
            break
    output = []
    for _ in range(len(nodes) * 2):
        output.append(current_node.value)
        current_node = nodes[current_node.n]
    print(output)


def insert_after(node, target_node, nodes):
    next_node = nodes[target_node.n]

    target_node.n = node.i
    node.p = target_node.i
    node.n = next_node.i
    next_node.p = node.i


def move(nodes, node, steps):
    current = node
    for _ in range(steps):
        current = nodes[current.n]
    return current


def do_part_1(nodes):
    print_nodes(nodes)
    for node in nodes:
        target_node = find_target(node, nodes)
        if target_node.n != node.i and node.value != 0:
            unlink_node(node, nodes)
            insert_after(node, target_node, nodes)

    zero_node = None
    for node in nodes:
        if node.value == 0:
            zero_node = node
            break
    th1000 = move(nodes, zero_node, 1000)
    th2000 = move(nodes, th1000, 1000)
    th3000 = move(nodes, th2000, 1000)
    v1, v2, v3 = th1000.value, th2000.value, th3000.value
    print(v1, v2, v3)
    return v1 + v2 + v3

    return "toto"


def do_part_2(processed_input):
    return "toto"
