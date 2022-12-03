import string


def priority(character):
    offset = 26 if character.isupper() else 0
    return string.ascii_lowercase.index(character.lower()) + 1 + offset


def process_input(blob):
    return [[priority(c) for c in line] for line in blob.split("\n")]


def do_part_1(rucksacks):
    priority_sum = 0
    for rucksack in rucksacks:
        middle = int(len(rucksack) / 2)
        priority_sum += {*rucksack[:middle]}.intersection({*rucksack[middle:]}).pop()
    return priority_sum


def do_part_2(rucksacks):
    priority_sum = 0
    for i in range(0, len(rucksacks), 3):
        elf1, elf2, elf3 = rucksacks[i], rucksacks[i + 1], rucksacks[i + 2]
        priority_sum += set(elf1).intersection(set(elf2)).intersection(set(elf3)).pop()
    return priority_sum
