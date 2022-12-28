from collections import defaultdict

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
    reactions = {}
    for command in blob.split("\n"):
        a, b, c = search_groups(r"^(.*)=([0-9]+)\*([\w]+)$", command)
        reactions[c] = Reaction(c, int(b), a)
    reactions["ORE"] = Reaction("ORE", 1, "")
    return reactions


def requires(element, reactions, needed, produced, n=1):
    if element == "ORE":
        return

    num_ores = 0
    for component, num in reactions[element].ingredients.items():
        have = produced[component] - needed[component]
        num_for_n = num * n

        if num_for_n > have:
            num_reactions = int(ceil((num_for_n - have) / reactions[component].num))

            needed[component] += num_for_n
            produced[component] += num_reactions * reactions[component].num
            requires(component, reactions, needed, produced, num_reactions)
        else:
            needed[component] += num_for_n
    return num_ores


def do_part_1(reactions):
    needed = defaultdict(int)
    produced = defaultdict(int)
    requires("FUEL", reactions, needed, produced)
    return produced["ORE"]


def binary_search(low, high, function):
    while high - low > 1:
        val = low + (high - low) // 2
        if function(val) > 1000000000000:
            high = val
        else:
            low = val
    return low


def do_part_2(reactions):
    def binary_search_function(n):
        needed = defaultdict(int)
        produced = defaultdict(int)
        requires("FUEL", reactions, needed, produced, n)
        return produced["ORE"]

    return binary_search(1, 10000000, binary_search_function)


def do_visualization(processed_input):
    return None
