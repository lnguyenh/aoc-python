from collections import deque


def get_neighbour(i, phrase):
    if phrase[i] == "?":
        return [".", "#"]
    return [phrase[i]]


def satisfies(path, code, phrase):
    combination = [len(blob) for blob in path.split(".") if blob]
    if combination:
        num_left_to_have = sum(code) - sum(combination)
        phrase_left = phrase[(len(path) - 1) :]
        if num_left_to_have > (phrase_left.count("#") + phrase_left.count("?")):
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
    #
    # Example of dynamic bfs to count all paths
    #
    paths = deque([""])

    count = 0
    length = len(phrase)
    while paths:
        path = paths.pop()

        for neighbour in get_neighbour(len(path), phrase):
            new_path = path + neighbour

            # Early break on condition
            if not satisfies(new_path, code, phrase):
                continue

            # Min break condition
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
    print(bfs_count("?.?.???????##???????.?.???????##?????", [1, 2, 8, 1, 2, 8]))
