from collections import defaultdict

ALPHABET = "AKQJT98765432"

COMBINATIONS = {(4,): 6, (3, 2): 5, (3,): 4, (2, 2): 3, (2,): 2, (1,): 1}
CARDS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
#
# ranks = []
# for c in ALPHABET:
#     for d in ALPHABET:
#         ranks.append({(c, 4), (d, 1)})
# for c in ALPHABET:
#     for d in ALPHABET:
#         ranks.append({(c, 3), (d, 2)})
# for c in ALPHABET:
#     for d in ALPHABET:
#         for e in ALPHABET:
#             ranks.append({(c, 3), (d, 1), (e, 1)})
# for c in ALPHABET:
#     for d in ALPHABET:
#         for e in ALPHABET:
#             ranks.append({(c, 3), (d, 1), (e, 1)})
# for c in ALPHABET:
#     for d in ALPHABET:
#         for e in ALPHABET:
#             ranks.append({(c, 3), (d, 1), (e, 1)})
#


def custom_sort(text):
    return sorted(text, key=lambda word: [ALPHABET.index(c) for c in word])


class Hand:
    def __init__(self, text, bid):
        self.text = text
        self.bid = int(bid)
        self.structure = self.get_structure()

        self.value = {
            "combination": 0,
            "one": 0,
            "two": 0,
            "three": 0,
            "four": 0,
            "five": 0,
        }
        self.set_value()

    def get_structure(self):
        structure = defaultdict(list)
        characters = set(self.text)
        for c in characters:
            structure[self.text.count(c)].append(c)
        return structure

    def set_value(self):
        combos = [count for count, _ in self.structure.items()]
        if 5 in combos:
            self.value["combination"] = 7
            self.value["one"] = CARDS[self.structure[5][0]]
        elif 4 in combos:
            self.value["combination"] = 6
            self.value["one"] = CARDS[self.structure[4][0]]
            self.value["two"] = CARDS[self.structure[1][0]]
        elif 3 in combos:
            if 2 in combos:
                self.value["combination"] = 5
                self.value["one"] = CARDS[self.structure[3][0]]
                self.value["two"] = CARDS[self.structure[2][0]]
            else:
                self.value["combination"] = 4
                self.value["one"] = CARDS[self.structure[3][0]]
                rest = custom_sort(self.structure[1])
                self.value["two"] = CARDS[rest[0]]
                self.value["three"] = CARDS[rest[1]]
        elif 2 in combos:
            if len(self.structure[2]) == 2:
                self.value["combination"] = 3
                pairs = custom_sort(self.structure[2])
                self.value["one"] = CARDS[pairs[0]]
                self.value["two"] = CARDS[pairs[1]]
                self.value["three"] = CARDS[self.structure[1][0]]
            else:
                self.value["combination"] = 2
                self.value["one"] = CARDS[self.structure[2][0]]
                rest = custom_sort(self.structure[1])
                self.value["two"] = CARDS[rest[0]]
                self.value["three"] = CARDS[rest[1]]
                self.value["four"] = CARDS[rest[2]]
        else:
            self.value["combination"] = 1
            rest = custom_sort(self.structure[1])
            self.value["one"] = CARDS[rest[0]]
            self.value["two"] = CARDS[rest[1]]
            self.value["three"] = CARDS[rest[2]]
            self.value["four"] = CARDS[rest[3]]
            self.value["five"] = CARDS[rest[4]]


def process_input(blob):
    lines = blob.split("\n")
    hands = []
    for line in lines:
        text, bid = line.split(" ")
        hand = Hand(text, bid)
        hands.append(hand)
    return hands


def do_part_1(hands):
    sorted_hands = sorted(
        hands,
        key=lambda hand: (
            hand.value["combination"],
            hand.value["one"],
            hand.value["two"],
            hand.value["three"],
            hand.value["four"],
            hand.value["five"],
        ),
    )
    result = 0
    for i, hand in enumerate(sorted_hands, start=1):
        to_add = i * hand.bid
        result += to_add
    return result


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
