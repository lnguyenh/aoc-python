from utils.strings import remove_from_string

OK = 1
TRY_RIGHT = 2
TRY_LEFT = 3


def process_input(blob):
    lines = blob.split("\n")
    times = [int(x) for x in lines[0].split(" ")[1:] if x]
    distances = [int(x) for x in lines[1].split(" ")[1:] if x]
    time_part_2 = int(remove_from_string(lines[0], ["Time:", " "]))
    distance_part_2 = int(remove_from_string(lines[1], ["Distance:", " "]))
    return times, distances, len(times), time_part_2, distance_part_2


class Race:
    def __init__(self, max_seconds, record_distance):
        self.max_seconds = max_seconds
        self.record_distance = record_distance

    def get_distance(self, seconds_pressed):
        speed = seconds_pressed
        travel_time = self.max_seconds - seconds_pressed
        return speed * travel_time

    def beats_record(self, seconds_pressed):
        return self.get_distance(seconds_pressed) > self.record_distance

    def get_speeds_beating_record(self):
        count = 0
        for seconds_pressed in range(self.max_seconds):
            if self.get_distance(seconds_pressed) > self.record_distance:
                count += 1
        return count

    def meets_left_bound_condition(self, index):
        left = self.beats_record(index)
        right = self.beats_record(index + 1)
        if not left and right:
            return OK
        elif left and right:
            return TRY_LEFT
        elif not left and not right:
            return TRY_RIGHT
        raise Exception("not reachable")

    def meets_right_bound_condition(self, index):
        left = self.beats_record(index)
        right = self.beats_record(index + 1)
        if left and not right:
            return OK
        elif left and right:
            return TRY_RIGHT
        elif not left and not right:
            return TRY_LEFT
        raise Exception("not reachable")

    def find_left_bound(self, start, stop):
        middle = int((start + stop) / 2)
        result = self.meets_left_bound_condition(middle)
        if result == OK:
            return middle + 1
        elif result == TRY_LEFT:
            return self.find_left_bound(start, middle)
        elif result == TRY_RIGHT:
            return self.find_left_bound(middle, stop)

    def find_right_bound(self, start, stop):
        middle = int((start + stop) / 2)
        result = self.meets_right_bound_condition(middle)
        if result == OK:
            return middle
        elif result == TRY_LEFT:
            return self.find_right_bound(start, middle)
        elif result == TRY_RIGHT:
            return self.find_right_bound(middle, stop)

    def get_speeds_beating_record_2(self):
        left = self.find_left_bound(0, self.max_seconds)
        right = self.find_right_bound(0, self.max_seconds)
        return right - left + 1


def do_part_1(processed_input):
    return "toto"
    times, distances, num_races, _, _ = processed_input
    num_speeds_beating_record = 1
    for i in range(num_races):
        race = Race(times[i], distances[i])
        num_speeds_beating_record = (
            num_speeds_beating_record * race.get_speeds_beating_record()
        )
    return num_speeds_beating_record


def do_part_2(processed_input):
    _, _, _, time, distance = processed_input
    race = Race(time, distance)
    return race.get_speeds_beating_record_2()
