from datetime import datetime
from importlib import import_module

import click

from utils.time import timedelta_in_ms

TEST_INPUT_DIRECTORY = "/inputs/test/"
INPUT_DIRECTORY = "/inputs/"


def get_input_path(year, day, test, filename):
    path = (
        f"year{year}{TEST_INPUT_DIRECTORY}" if test else f"year{year}{INPUT_DIRECTORY}"
    )
    filename = filename if filename else f"{day}.txt"
    return path + filename


@click.command()
@click.option("--year", default="", help="AOC year to run")
@click.option("--day", default="", help="AOC day to run")
@click.option("--test", is_flag=True)
@click.option("--filename", default="", help="Input file name")
@click.option("--visu", is_flag=True)
def run(year, day, test, filename, visu):
    # Setup
    if not year:
        # Use today's year
        year = datetime.now().strftime("%Y")
    if not day:
        # Use today's day of the month
        day = datetime.now().strftime("%d")
    input_path = get_input_path(year, day, test, filename)
    print(f"Running AOC day {day}{' IN TEST MODE' if test else ''} using {input_path}")

    # Import the module for the day
    day_module = import_module(f"year{year}.days.{day}")

    # Read the raw input
    with open(input_path, "r") as file:
        raw_input = file.read()

    # Get processed input
    processed_input = day_module.process_input(raw_input)

    # Visualization
    if visu:
        day_module.do_visualization(processed_input)
        return

    # Run part 1
    t0 = datetime.now()
    answer_1 = day_module.do_part_1(processed_input)
    t1 = datetime.now()

    # Run part 2
    answer_2 = day_module.do_part_2(processed_input)
    t2 = datetime.now()

    # Finish
    print(f"Part 1: {answer_1} ({timedelta_in_ms(t1, t0)}ms)")
    print(f"Part 2: {answer_2} ({timedelta_in_ms(t2, t1)}ms)")
    print(f"Done in {timedelta_in_ms(t2, t0)}ms")


if __name__ == "__main__":
    run()
