import functools

NUM_TURNS = 24

num_bots = 1
PRODUCED = []
for _ in range(NUM_TURNS):
    already_produced = sum(PRODUCED)
    PRODUCED.append(num_bots + already_produced)
    num_bots += 1


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

        self.current_best = 0
        self.earliest_geode_bot_turn = None
        self.earliest_obsidian_bot_turn = None
        self.earliest_clay_bot_turn = None

        self.reached_end_once = False

        self.last_turn_to_get_one_obsidian_bot = None
        for i in range(len(PRODUCED) - 1):
            if PRODUCED[i] <= self.blueprint["geode"][1] < PRODUCED[i + 1]:
                self.last_turn_to_get_one_obsidian_bot = (NUM_TURNS - 1) - (i + 1) - 1

        self.last_turn_to_get_one_clay_bot = None
        for i in range(len(PRODUCED) - 1):
            if PRODUCED[i] <= self.blueprint["obsidian"][1] < PRODUCED[i + 1]:
                self.last_turn_to_get_one_clay_bot = (
                    self.last_turn_to_get_one_obsidian_bot - (i + 1) - 1
                )
        self.toto = 1

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
        return tuple(new_resources)

    def get_new_robots(self, robots, i):
        new_robots = list(robots)
        new_robots[i] += 1
        return tuple(new_robots)

    def resources_post_purchase(self, resources, i):
        new_resources = list(resources)
        if i == 0:
            new_resources[0] -= self.blueprint["ore"]
        elif i == 1:
            new_resources[0] -= self.blueprint["clay"]
        elif i == 2:
            new_resources[0] -= self.blueprint["obsidian"][0]
            new_resources[1] -= self.blueprint["obsidian"][1]
        elif i == 3:
            new_resources[0] -= self.blueprint["geode"][0]
            new_resources[2] -= self.blueprint["geode"][1]
        return tuple(new_resources)

    @functools.cache
    def find_best_path(self, robots, resources, i):

        if i == NUM_TURNS:
            if not self.reached_end_once:
                self.reached_end_once = True
            return resources[3]

        # we receive our resources for this turn
        new_resources = self.get_new_resources(robots, resources)

        possibles = []

        if self.has_enough_for_geode_robot(resources):  # based on old resources
            new_robots = self.get_new_robots(robots, 3)
            updated_new_resources = self.resources_post_purchase(new_resources, 3)
            possibles.append((new_robots, updated_new_resources, i + 1))

            if self.earliest_geode_bot_turn is None or i < self.earliest_geode_bot_turn:
                self.earliest_geode_bot_turn = i

        if self.has_enough_for_obsidian_robot(resources):  # based on old resources
            new_robots = self.get_new_robots(robots, 2)
            updated_new_resources = self.resources_post_purchase(new_resources, 2)
            possibles.append((new_robots, updated_new_resources, i + 1))

            if (
                self.earliest_obsidian_bot_turn is None
                or i < self.earliest_obsidian_bot_turn
            ):
                self.earliest_obsidian_bot_turn = i

        if self.has_enough_for_clay_robot(resources):  # based on old resources
            new_robots = self.get_new_robots(robots, 1)
            updated_new_resources = self.resources_post_purchase(new_resources, 1)
            possibles.append((new_robots, updated_new_resources, i + 1))

            if self.earliest_clay_bot_turn is None or i < self.earliest_clay_bot_turn:
                self.earliest_clay_bot_turn = i

        if self.has_enough_for_ore_robot(resources):  # based on old resources
            new_robots = self.get_new_robots(robots, 0)
            updated_new_resources = self.resources_post_purchase(new_resources, 0)
            possibles.append((new_robots, updated_new_resources, i + 1))

        new_robots = robots[:]
        possibles.append((new_robots, new_resources, i + 1))

        for possible in possibles:
            # try to break out as early as possible
            if (
                (
                    possible[0][3] == 0
                    and self.earliest_geode_bot_turn
                    and i + 1 > self.earliest_geode_bot_turn
                )
                or (
                    possible[0][2] == 0
                    and i + 1 >= self.last_turn_to_get_one_obsidian_bot
                )
                or (possible[0][1] == 0 and i + 1 >= self.last_turn_to_get_one_clay_bot)
                or ((i + 1) >= NUM_TURNS - 1 and possible[0][3] == 0)
            ):
                continue
            num_geodes = self.find_best_path(*possible)
            if num_geodes > self.current_best:
                self.current_best = num_geodes
        return self.current_best


def do_part_1(blueprints):
    geodes = []
    for name, blueprint in blueprints:
        factory = Factory(name, blueprint)
        m = factory.find_best_path((1, 0, 0, 0), (0, 0, 0, 0), 0)
        print(f"{factory.name} - max: {m}")
        geodes.append((m, int(factory.name)))
    print(geodes)

    return sum([a * b for a, b in geodes])


def do_part_2(processed_input):
    return "toto"
