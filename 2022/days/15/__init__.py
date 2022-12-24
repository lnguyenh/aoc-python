def simplify(intervals):
    results = []
    building = False
    opened = set()
    for i in sorted(intervals, key=lambda x: x[0]):
        val, val_type, sensor_index = i

        if val_type == "start":
            opened.add(sensor_index)
        else:
            opened.remove(sensor_index)

        if not building:
            results.append(i)
            building = True
            continue
        else:
            if len(opened) == 0:
                results.append(i)
                building = False
    return results


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
    if len(sensors) > 20:
        TARGET_Y = 2000000
    else:
        TARGET_Y = 10

    forbidden = set()
    for i, sensor in enumerate(sensors):
        result = sensor.forbidden_xs(TARGET_Y)
        if result:
            x1, x2 = result
            for x in range(x1, x2 + 1):
                forbidden.add(x)
    for i, sensor in enumerate(sensors):
        if sensor.beacon.y == TARGET_Y and sensor.beacon.x in forbidden:
            forbidden.remove(sensor.beacon.x)
    return len(forbidden)


def do_part_2(sensors):
    if len(sensors) > 20:
        MAX = 4000000
    else:
        MAX = 20

    result_y = None
    result_x = None
    for y in range(MAX + 1):
        intervals = []
        for i, sensor in enumerate(sensors):
            result = sensor.forbidden_xs(y)
            if result:
                x1, x2 = result
                intervals.append((x1, "start", i))
                intervals.append((x2, "end", i))
        simplified = simplify(intervals)
        found = False
        for i in range(len(simplified) - 1):
            i1, i2 = simplified[i], simplified[i + 1]
            if i2[0] - i1[0] == 2 and i1[1] == "end" and i2[1] == "start":
                result_y = y
                result_x = i1[0] + 1
                if 0 <= result_x <= MAX:
                    found = True
                    break
        if found:
            break

    return result_x * 4000000 + result_y
