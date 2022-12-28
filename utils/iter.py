from itertools import combinations


def chunk_iter(iterable, chunk_size):
    return zip(*(iter(iterable),) * chunk_size)


if __name__ == "__main__":
    text = "1234567"
    print(f"Chunking a list/tuple/string/... {text} chunked in elements of size 3")
    print(list(chunk_iter(text, 3)))
    print()

    l = [1, 2, 3, 4, 5]
    print(
        f"Combinations of n elements from a list. Example combinations of 2 elements "
        f"from {l}"
    )
    print(list(combinations(l, 2)))
