def process_input(blob):
    blob = (
        blob.replace("Blueprint", "")
        .replace("ore", "")
        .replace("clay", "")
        .replace("obsidian", "")
        .replace("geode", "")
        .replace(" ", "")
        .replace("Eachrobotcosts", "")
    )
    lines = blob.split("\n")
    blueprints = []
    for line in lines:
        blueprint_id, rest = line.split(":")
        ore, clay, obsidian, geode, _ = rest.split(".")
        blueprints.append(
            (
                blueprint_id,
                {
                    "ore": int(ore),
                    "clay": int(clay),
                    "obsidian": [int(x) for x in obsidian.split("and")],
                    "geode": [int(x) for x in geode.split("and")],
                },
            )
        )
    return blueprints


class Factory:
    def __init__(self, name, blueprint):
        self.name = name
        self.blueprint = blueprint
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

        self.ores = 0
        self.clays = 0
        self.obsidians = 0
        self.geodes = 0

    def one_minute(self):
        self.spend()
        self.harvest()
        self.harvest_robot()

    def build_nodes(self):
        nodes = {}
        for i in reversed(range(24)):
            if i == 23:
                nodes[f"or-{i}"] = []
                nodes[f"c-{i}"] = []
                nodes[f"ob-{i}"] = []
                nodes[f"g-{i}"] = []
            else:
                nodes[f"or-{i}"] = [f"or-{i}", f"c-{i}", f"ob-{i}", f"g-{i}"]
                nodes[f"c-{i}"] = [f"or-{i}", f"c-{i}", f"ob-{i}", f"g-{i}"]
                nodes[f"ob-{i}"] = [f"or-{i}", f"c-{i}", f"ob-{i}", f"g-{i}"]
                nodes[f"g-{i}"] = [f"or-{i}", f"c-{i}", f"ob-{i}", f"g-{i}"]
        return nodes

    def has_enough_for_ore_robot(self, resources):
        return self.blueprint["ore"] <= resources[0]

    def has_enough_for_clay_robot(self, resources):
        return self.blueprint["clay"] <= resources[0]

    def has_enough_for_obsidian_robot(self, resources):
        return (
            self.blueprint["obsidian"][0] <= resources[0]
            and self.blueprint["obsidian"][1] <= resources[1]
        )

    def has_enough_for_geode_robot(self, resources):
        return (
            self.blueprint["geode"][0] <= resources[0]
            and self.blueprint["geode"][1] <= resources[2]
        )

    def get_new_resources(self, robots, resources):
        new_resources = []
        for i in range(len(robots)):
            new_resources.append(robots[i] + resources[i])
        return new_resources

    def get_new_robots(self, robots, i):
        new_robots = robots[:]
        new_robots[i] += 1
        return new_robots

    def find_best_path(self, robots, resources, i):
        if i > 23:
            return robots[3] + resources[3]

        possibles = []

        new_resources = self.get_new_resources(robots, resources)

        if self.has_enough_for_ore_robot(resources):
            made_one = True
            new_robots = self.get_new_robots(robots, 0)
            possibles.append((new_robots, new_resources, i + 1))

        if self.has_enough_for_clay_robot(resources):
            new_robots = self.get_new_robots(robots, 1)
            possibles.append((new_robots, new_resources, i + 1))

        if self.has_enough_for_obsidian_robot(resources):
            new_robots = self.get_new_robots(robots, 2)
            possibles.append((new_robots, new_resources, i + 1))

        if self.has_enough_for_geode_robot(resources):
            new_robots = self.get_new_robots(robots, 3)
            possibles.append((new_robots, new_resources, i + 1))

        new_robots = robots[:]
        possibles.append((new_robots, new_resources, i + 1))

        return max([self.find_best_path(*possible) for possible in possibles])

    def harvest(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidians += self.obsidian_robots
        self.geodes += self.geode_robots

    def spend(self):
        return

    def harvest_robot(self):
        return


def do_part_1(blueprints):
    geodes = []
    for name, blueprint in blueprints:
        factory = Factory(name, blueprint)
        geodes.append(factory.find_best_path([1, 0, 0, 0], [0, 0, 0, 0], 0))
    return "toto"


def do_part_2(processed_input):
    return "toto"
