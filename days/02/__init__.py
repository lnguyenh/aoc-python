PLAY_TO_SCORE = {
    "AX": 1 + 3,
    "AY": 2 + 6,
    "AZ": 3,
    "BX": 1,
    "BY": 2 + 3,
    "BZ": 3 + 6,
    "CX": 1 + 6,
    "CY": 2,
    "CZ": 3 + 3,
}

# Translate a part-2 string to a part-1 desired play
# X lose, Y draw, Z win
DESIRED_OUTCOME_TO_PLAY = {
    "AX": "AZ",
    "BX": "BX",
    "CX": "CY",
    "AY": "AX",
    "BY": "BY",
    "CY": "CZ",
    "AZ": "AY",
    "BZ": "BZ",
    "CZ": "CX",
}


def process_input(blob):
    return blob.replace(" ", "").split("\n")


def do_part_1(plays):
    return sum([PLAY_TO_SCORE[play] for play in plays])


def do_part_2(desired_outcomes):
    plays = [DESIRED_OUTCOME_TO_PLAY[outcome] for outcome in desired_outcomes]
    return sum([PLAY_TO_SCORE[play] for play in plays])
