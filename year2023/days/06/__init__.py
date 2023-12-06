def process_input(blob):
    lines = blob.split("\n")
    times = [int(x) for x in lines[0].split(" ")[1:] if x]
    distances = [int(x) for x in lines[1].split(" ")[1:] if x]
    return times, distances, len(times)


class Race:
    def __init__(self, max_seconds, record_distance):
        self.max_seconds = max_seconds
        self.record_distance = record_distance

    def get_distance(self, seconds_pressed):
        speed = seconds_pressed
        travel_time = self.max_seconds - seconds_pressed
        return speed * travel_time

    def get_speeds_beating_record(self):
        count = 0
        for seconds_pressed in range(self.max_seconds):
            if self.get_distance(seconds_pressed) > self.record_distance:
                count += 1
        return count


def do_part_1(processed_input):
    times, distances, num_races = processed_input
    num_speeds_beating_record = 1
    for i in range(num_races):
        race = Race(times[i], distances[i])
        num_speeds_beating_record = (
            num_speeds_beating_record * race.get_speeds_beating_record()
        )
    return num_speeds_beating_record


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
