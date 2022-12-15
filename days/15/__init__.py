class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sensor:
    def __init__(self, xs, ys, xb, yb):
        self.position = Point(int(xs), int(ys))
        self.beacon = Point(int(xb), int(yb))

    @property
    def distance(self):
        return abs(self.position.x - self.beacon.x) + abs(
            self.position.y - self.beacon.y
        )

    def forbidden_xs(self, y):
        dx = abs(y - self.position.y) - self.distance
        if dx > 0:
            return None
        else:
            return self.position.x + dx, self.position.x - dx


def process_input(blob):
    blob = (
        blob.replace("Sensor at ", "")
        .replace(": closest beacon is at ", ", ")
        .replace("x=", "")
        .replace("y=", "")
    )
    lines = blob.split("\n")
    sensors = []
    for line in lines:
        xs, ys, xb, yb = line.split(", ")
        sensors.append(Sensor(xs, ys, xb, yb))
    return sensors


def do_part_1(sensors):
    TARGET_Y = 2000000
    forbidden = set()
    for i, sensor in enumerate(sensors):
        result = sensor.forbidden_xs(TARGET_Y)
        if result:
            x1, x2 = result
            # print(f"{i} {x1} {x2}")
            for x in range(x1, x2 + 1):
                forbidden.add(x)
    for i, sensor in enumerate(sensors):
        if sensor.beacon.y == TARGET_Y and sensor.beacon.x in forbidden:
            forbidden.remove(sensor.beacon.x)
    return len(forbidden)


def do_part_2(processed_input):
    return "toto"
