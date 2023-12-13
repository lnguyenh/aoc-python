from collections import deque


def get_neighbour(i, phrase):
    if phrase[i] == "?":
        return [".", "#"]
    return [phrase[i]]


def satisfies(path, code, max_length):
    combination = [len(blob) for blob in path.split(".") if blob]
    if combination:
        if sum(code) - sum(combination) > (max_length - len(path)):
            return False
    if len(combination) > len(code):
        return False
    if path.endswith("."):
        return combination == code[: len(combination)]
    else:
        return (
            combination[:-1] == code[: len(combination) - 1]
            and combination[-1] <= code[len(combination) - 1]
        )


def satisfies_fully(path, code):
    combination = [len(blob) for blob in path.split(".") if blob]
    return combination == code


def bfs_count(phrase, code):
    paths = deque([""])

    count = 0
    length = len(phrase)
    while paths:
        path = paths.pop()

        for neighbour in get_neighbour(len(path), phrase):
            new_path = path + neighbour

            if not satisfies(new_path, code, length):
                continue

            if len(new_path) == length:
                if satisfies_fully(new_path, code):
                    # print(new_path)
                    count += 1
            else:
                paths.append(new_path)
    return count


if __name__ == "__main__":
    print(bfs_count("????.#...#...", [4, 1, 1]))
    print(bfs_count("?#?#?#?#?#?#?#?", [1, 3, 1, 6]))
    print(bfs_count("?###????????", [3, 2, 1]))
