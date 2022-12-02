from datetime import datetime
from importlib import import_module

import click

from utils.time import get_time_delta

TEST_INPUT_DIRECTORY = "./inputs/test/"
INPUT_DIRECTORY = "./inputs/"


def get_input_path(day, test, filename):
    path = TEST_INPUT_DIRECTORY if test else INPUT_DIRECTORY
    filename = filename if filename else f"{day}.txt"
    return path + filename


@click.command()
@click.option("--day", default="01", help="AOC day to run")
@click.option("--test", is_flag=True)
@click.option("--filename", default="", help="Input file name")
def run(day, test, filename):
    if not day:
        # Use today's day of the month
        day = datetime.now().strftime("%d")

    # Import the module for the day
    day_module = import_module(f"days.{day}")

    input_path = get_input_path(day, test, filename)

    print(f"Running AOC day {day}{' IN TEST MODE' if test else ''} using {input_path}")

    # Read the raw input
    with open(input_path, "r") as file:
        blob = file.read()

    # Get processed input
    processed_input = day_module.process_input(blob)

    # Run part 1
    t0 = datetime.now()
    answer_1 = day_module.do_part_1(processed_input)
    t1 = datetime.now()

    # Run part 2
    answer_2 = day_module.do_part_2(processed_input)
    t2 = datetime.now()

    # Finish
    print(f"Part 1: {answer_1} ({get_time_delta(t1, t0)}ms)")
    print(f"Part 2: {answer_2} ({get_time_delta(t2, t1)}ms)")
    print(f"Done in {get_time_delta(t2, t0)}ms")


if __name__ == "__main__":
    run()
