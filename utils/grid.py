def get_name(x, y):
    # Transforms xy coordinates to a key string
    # Can be used when using a dict to represent a grid
    return f"{x}.{y}"


def name_to_xy(name):
    # Transforms a key string to xy coordinates
    # Can be used when using a dict to represent a grid
    x, y = name.split(".")
    return int(x), int(y)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x={self.x}, y={self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(tuple((self.x, self.y)))
