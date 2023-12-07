from collections import defaultdict

ALPHABET = "AKQJT98765432"
ALPHABET_2 = "AKQT98765432J"

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

CARDS_2 = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def custom_sort(text):
    return sorted(text, key=lambda word: [ALPHABET.index(c) for c in word])


def custom_sort_2(text):
    return sorted(text, key=lambda word: [ALPHABET_2.index(c) for c in word])


class Hand:
    def __init__(self, text, bid):
        self.text = text
        self.bid = int(bid)
        self.structure = self.get_structure()
        self.part_1_values = [CARDS[c] for c in text]

        self.value = {
            "combination": 0,
        }
        self.set_value()

    def __repr__(self):
        s = sorted(
            [x for x in self.structure.items()], key=lambda z: z[0], reverse=True
        )
        text = ""
        for count, characters in s:
            for c in custom_sort(characters):
                text += c * count
        return text

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
        elif 4 in combos:
            self.value["combination"] = 6
        elif 3 in combos:
            if 2 in combos:
                self.value["combination"] = 5
            else:
                self.value["combination"] = 4
        elif 2 in combos:
            if len(self.structure[2]) == 2:
                self.value["combination"] = 3
            else:
                self.value["combination"] = 2
                self.value["one"] = CARDS[self.structure[2][0]]
                rest = custom_sort(self.structure[1])
                self.value["two"] = CARDS[rest[0]]
                self.value["three"] = CARDS[rest[1]]
                self.value["four"] = CARDS[rest[2]]
        elif 1 in combos:
            self.value["combination"] = 1
            rest = custom_sort(self.structure[1])
            self.value["one"] = CARDS[rest[0]]
            self.value["two"] = CARDS[rest[1]]
            self.value["three"] = CARDS[rest[2]]
            self.value["four"] = CARDS[rest[3]]
            self.value["five"] = CARDS[rest[4]]
        else:
            raise Exception


class HandPart2:
    def __init__(self, text, bid):
        self.text = text
        self.bid = int(bid)
        self.structure = self.get_structure()
        self.num_js = self.text.count("J")
        self.apply_js()
        self.part_1_values = [CARDS_2[c] for c in text]

        self.value = {
            "combination": 0,
        }
        self.set_value()

    def apply_js(self):
        if self.structure:
            max_key = max(self.structure.keys())
        else:
            max_key = 0
        if max_key:
            tmp = self.structure[max_key]
            if len(self.structure[max_key]) == 1:
                self.structure.pop(max_key)
        else:
            tmp = "toto"
        self.structure[max_key + self.num_js] = tmp

    def __repr__(self):
        s = sorted(
            [x for x in self.structure.items()], key=lambda z: z[0], reverse=True
        )
        text = ""
        for count, characters in s:
            for c in custom_sort_2(characters):
                text += c * count
        return text

    def get_structure(self):
        structure = defaultdict(list)
        characters = set(self.text)
        for c in characters:
            if c != "J":
                structure[self.text.count(c)].append(c)
        return structure

    def set_value(self):
        combos = [count for count, _ in self.structure.items()]
        if 5 in combos:
            self.value["combination"] = 7
        elif 4 in combos:
            self.value["combination"] = 6
        elif 3 in combos:
            if 2 in combos:
                self.value["combination"] = 5
            else:
                self.value["combination"] = 4
        elif 2 in combos:
            if len(self.structure[2]) == 2:
                self.value["combination"] = 3
            else:
                self.value["combination"] = 2
        elif 1 in combos:
            self.value["combination"] = 1
        else:
            raise Exception


def process_input(blob):
    lines = blob.split("\n")
    hands = []
    hands_2 = []
    for line in lines:
        text, bid = line.split(" ")
        hand = Hand(text, bid)
        hands.append(hand)
        hands_2.append(HandPart2(text, bid))
    return hands, hands_2


def do_part_1(processed_input):
    hands, _ = processed_input
    sorted_hands = sorted(
        hands,
        key=lambda hand: (
            hand.value["combination"],
            hand.part_1_values[0],
            hand.part_1_values[1],
            hand.part_1_values[2],
            hand.part_1_values[3],
            hand.part_1_values[4],
        ),
    )
    result = 0
    for i, hand in enumerate(sorted_hands, start=1):
        to_add = i * hand.bid
        result += to_add
    return result


def do_part_2(processed_input):
    _, hands = processed_input
    sorted_hands = sorted(
        hands,
        key=lambda hand: (
            hand.value["combination"],
            hand.part_1_values[0],
            hand.part_1_values[1],
            hand.part_1_values[2],
            hand.part_1_values[3],
            hand.part_1_values[4],
        ),
    )
    result = 0
    for i, hand in enumerate(sorted_hands, start=1):
        to_add = i * hand.bid
        result += to_add
    return result


def do_visualization(processed_input):
    return None
