string_to_score = {
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
string_to_play = {
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


def do_part_1(processed_input):
    return sum([string_to_score[text] for text in processed_input])


def do_part_2(processed_input):
    plays = [string_to_play[text] for text in processed_input]
    return sum([string_to_score[text] for text in plays])
