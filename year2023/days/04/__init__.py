from collections import defaultdict


def process_input(blob):
    raw_lines = blob.split("\n")
    winning_numbers = []
    owned_numbers = []
    for raw_line in raw_lines:
        line = raw_line.replace(": ", ";")
        line = line.replace(" | ", ";")
        _, winning, owned = line.split(";")
        winning_numbers.append(
            set([int(number) for number in winning.split(" ") if number])
        )
        owned_numbers.append(
            set([int(number) for number in owned.split(" ") if number])
        )
    return winning_numbers, owned_numbers


def do_part_1(processed_input):
    winning_numbers, owned_numbers = processed_input
    count = 0
    for i in range(len(winning_numbers)):
        matches = winning_numbers[i].intersection(owned_numbers[i])
        if matches:
            to_add = pow(2, len(matches) - 1)
            count += to_add
    return count


def do_part_2(processed_input):
    winning_numbers, owned_numbers = processed_input

    targets = defaultdict(int)  # how many cards we win for each card number
    card_counts = {}
    cards_to_process = {}

    for i in range(len(winning_numbers)):
        card_counts[i + 1] = 0
        cards_to_process[i + 1] = 1

    for i in range(len(winning_numbers)):
        matches = winning_numbers[i].intersection(owned_numbers[i])
        if matches:
            targets[i + 1] = len(matches)

    while cards_to_process:
        new_cards_to_process = defaultdict(int)
        for card_number, amount in cards_to_process.items():
            for _ in range(amount):
                card_counts[card_number] += 1
                for i in range(targets[card_number]):
                    card_won_index = card_number + i + 1
                    if card_won_index > len(winning_numbers):
                        break
                    new_cards_to_process[card_won_index] += 1
        cards_to_process = new_cards_to_process

    count = 0
    for _, num_cards in card_counts.items():
        count += num_cards
    return count
