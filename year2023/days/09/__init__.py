class Series:
    def __init__(self, line):
        self.values = {}
        for i, value in enumerate(line):
            self.values[(0, i)] = value

        self.depth = 0
        self.width = len(line)
        self.original_width = self.width

        self.dig()

    def is_ready(self):
        return all([self.values[(self.depth, i)] == 0 for i in range(self.width)])

    def dig(self):
        depth = self.depth
        new_depth = self.depth + 1
        for i in range(self.width - 1):
            self.values[(new_depth, i)] = (
                self.values[(depth, i + 1)] - self.values[(depth, i)]
            )
        self.depth = new_depth
        self.width = self.width - 1

    def dig_to_bottom(self):
        while not self.is_ready():
            self.dig()

    def extrapolate(self):
        depth = self.depth
        width = self.width

        # bottom line
        self.values[(depth, width)] = 0
        width += 1
        depth -= 1
        self.width += 1

        new_value = None
        while True:
            new_value = (
                self.values[(depth, width - 1)] + self.values[(depth + 1, width - 1)]
            )
            self.values[(depth, width)] = new_value
            width += 1
            depth -= 1
            if depth < 0:
                break
        return new_value

    def print(self):
        width = self.original_width + 1
        for d in range(self.depth + 1):
            line = ""
            for i in range(width):
                line += f"{self.values.get((d, i), 'x')} "
            print(line)
            width -= 1
        print("\n")


def process_input(blob):
    lines = blob.split("\n")
    return [Series([int(x) for x in line.split(" ")]) for line in lines]


def do_part_1(all_series):
    count = 0
    for series in all_series:
        series.dig_to_bottom()
        count += series.extrapolate()

    return count


def do_part_2(lines):
    return "toto"


def do_visualization(processed_input):
    return None
