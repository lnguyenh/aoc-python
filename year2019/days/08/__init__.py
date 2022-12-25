def process_input(blob):
    return blob


def do_part_1(text):
    min_num_zeros = None
    result = None
    for chunk in zip(*(iter(text),) * (25 * 6)):
        num_zeros = chunk.count("0")
        if min_num_zeros is None or num_zeros < min_num_zeros:
            min_num_zeros = num_zeros
            result = chunk.count("1") * chunk.count("2")
    return result


def do_part_2(text):
    chunks = list(zip(*(iter(text),) * (25 * 6)))

    image = []
    for i in range(len(chunks[0])):
        for j in range(len(chunks)):
            if chunks[j][i] != "2":
                image.append(chunks[j][i])
                break

    for chunk in zip(*(iter(image),) * 25):
        print("".join(chunk).replace("1", "*").replace("0", " "))
    return "toto"


def do_visualization(processed_input):
    return None
