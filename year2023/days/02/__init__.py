import re

RED = "red"
GREEN = "green"
BLUE = "blue"


def process_input(blob):
    games = []
    for line in blob.split("\n"):
        raw_game = re.split("[,|;]", line.split(":")[1])
        games.append([combination.strip().split(" ") for combination in raw_game])
    return games


def do_part_1(games):
    count = 0
    for i, game in enumerate(games, start=1):
        for quantity, color in game:
            q = int(quantity)
            if (
                (color == RED and q > 12)
                or (color == GREEN and q > 13)
                or (color == BLUE and q > 14)
            ):
                break
        else:
            count += i
    return count


def do_part_2(games):
    count = 0
    for i, game in enumerate(games):
        minimums = {RED: 0, BLUE: 0, GREEN: 0}
        for quantity, color in game:
            q = int(quantity)
            if color == RED and minimums[RED] < q:
                minimums[RED] = q
            elif color == BLUE and minimums[BLUE] < q:
                minimums[BLUE] = q
            elif color == GREEN and minimums[GREEN] < q:
                minimums[GREEN] = q
        count += minimums[RED] * minimums[GREEN] * minimums[BLUE]
    return count
