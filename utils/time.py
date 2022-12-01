def get_time_delta(timestamp_2, timestamp_1):
    diff = timestamp_2 - timestamp_1
    return round(diff.total_seconds() * 1000, 5)
