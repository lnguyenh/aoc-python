from collections import defaultdict, deque

from math import ceil

from utils.regexp import search_groups


class Reaction:
    def __init__(self, what, num, ingredients):
        self.what = what
        self.num = num
        self.ingredients = {}
        if ingredients:
            for combi in ingredients.split("+"):
                how_many, x = combi.split("*")
                self.ingredients[x] = int(how_many)


def process_input(blob):
    blob = blob.replace(" => ", "=")
    blob = blob.replace(", ", "+")
    blob = blob.replace(" ", "*")
    return blob.split("\n")


def requires(element, reactions, needed, produced):
    if element == "ORE":
        return

    num_ores = 0
    for component, num in reactions[element].ingredients.items():
        have = produced[component] - needed[component]

        if num > have:
            num_reactions = int(ceil((num - have) / reactions[component].num))

            needed[component] += num
            produced[component] += num_reactions * reactions[component].num
            for _ in range(num_reactions):
                requires(component, reactions, needed, produced)
        else:
            needed[component] += num
    return num_ores


def dynamic_bfs(start, destination, state, get_neighbours):
    paths = deque([[start]])
    while paths:
        path = paths.pop()
        node = path[-1]

        for neighbour in get_neighbours(state):
            new_path = list(path)
            new_path.append(neighbour)

            if neighbour == destination:
                return len(new_path), new_path

            paths.append(new_path)
            visited[node] = True


def do_part_1(commands):
    reactions = {}
    for command in commands:
        a, b, c = search_groups(r"^(.*)=([0-9]+)\*([\w]+)$", command)
        reactions[c] = Reaction(c, int(b), a)
    reactions["ORE"] = Reaction("ORE", 1, "")
    needed = defaultdict(int)
    produced = defaultdict(int)
    requires("FUEL", reactions, needed, produced)

    return produced["ORE"]


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
