def process_input(blob):
    return blob.split(",")


def do_part_1(processed_input):
    hashes = []
    for word in processed_input:
        cv = 0
        for c in word:
            cv += ord(c)
            cv *= 17
            cv = cv % 256
        hashes.append(cv)
    return sum(hashes)


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
