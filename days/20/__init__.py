from collections import deque


class Number:
    def __init__(self, number, position):
        self.name = chr(ord("a") + position)
        self.value = number

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value} ({self.name})"


def process_input(blob):
    return [Number(int(x), i) for i, x in enumerate(blob.split("\n"))]


def move_one_step_right(name, deck):
    # pop everything until we have n in our hands
    popped = deque()
    n = None
    while True:
        n = deck.popleft()
        if n.name == name:
            break
        popped.append(n)

    if not n:
        raise Exception("toti")

    if not deck:
        while popped:
            deck.appendleft(popped.pop())
        popped.append(deck.popleft())
        deck.appendleft(n)
        deck.appendleft(popped.pop())
    else:
        popped.append(deck.popleft())
        deck.appendleft(n)
        while popped:
            deck.appendleft(popped.pop())
    return deck


def move_one_step_left(name, deck):
    # pop everything until we have n in our hands
    popped = deque()
    n = None
    while True:
        n = deck.popleft()
        if n.name == name:
            break
        popped.append(n)

    if not n:
        raise Exception("toto")

    if not popped:
        popped.append(deck.pop())
        deck.append(n)
        deck.append(popped.pop())
    else:
        deck.appendleft(popped.pop())
        if not popped:
            deck.append(n)
        else:
            deck.appendleft(n)
            while popped:
                deck.appendleft(popped.pop())
    return deck


def do_part_1(numbers):
    deck = deque(numbers)
    names = [n.name for n in numbers]
    as_dict = {n.name: n for n in numbers}

    for name in names:
        n = as_dict[name]
        steps = n.value
        if steps > 0:
            for _ in range(steps):
                move_one_step_right(name, deck)
                toto = 0
        else:
            for _ in range(-steps):
                move_one_step_left(name, deck)
                toto = 0
    i = 0
    for n in deck:
        if n.value == 0:
            break
        i += 1
    th1000 = (i + 1000) % len(deck)
    th2000 = (i + 2000) % len(deck)
    th3000 = (i + 3000) % len(deck)
    a, b, c = deck[th1000].value, deck[th2000].value, deck[th3000].value
    return a + b + c


def do_part_2(processed_input):
    return "toto"
