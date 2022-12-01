def get_elf_calories(blob):
    return sum([int(x) for x in blob.split("\n")])


def process_input(blob):
    return blob.split("\n\n")


def do_part_1(calories):
    max_calories = 0
    for elf_blob in calories:
        max_calories = max(max_calories, get_elf_calories(elf_blob))
    return max_calories


def do_part_2(calories):
    all_calories = []
    for elf_blob in calories:
        all_calories.append(get_elf_calories(elf_blob))
    all_calories.sort(reverse=True)
    return sum(all_calories[:3])
