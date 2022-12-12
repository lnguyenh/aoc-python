def get_name(x, y):
    # Transforms xy coordinates to a key string
    # Can be used when using a dict to represent a grid
    return f"{x}.{y}"


def name_to_xy(name):
    # Transforms a key string to xy coordinates
    # Can be used when using a dict to represent a grid
    x, y = name.split(".")
    return int(x), int(y)
