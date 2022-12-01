from datetime import datetime
from importlib import import_module

import click

from utils.time import get_time_delta

TEST_INPUT_DIRECTORY = "./inputs/test/"
INPUT_DIRECTORY = "./inputs/"


@click.command()
@click.option("--day", default=0, help="AOC day to run")
@click.option("--test", is_flag=True)
@click.option("--filename", default="", help="Input file name")
def run(day, test, filename):
    if not day:
        day = datetime.now().strftime("%d")

    print(f"Running AOC day {day}")

    # Import the module for the wanted day
    day_module_name = f"days.{day}"
    day_module = import_module(day_module_name)

    # Get the input blob
    path = TEST_INPUT_DIRECTORY if test else INPUT_DIRECTORY
    filename = filename if filename else f"{day}.txt"
    input_file_path = path + filename
    print(f"Using input {input_file_path}")
    with open(input_file_path, "r") as file:
        blob = file.read()

    # Get processed input
    processed_input = day_module.process_input(blob)

    # Run part 1
    t0 = datetime.now()
    answer_1 = day_module.do_part_1(processed_input)
    t1 = datetime.now()
    print(f"Part 1: {answer_1} ({get_time_delta(t1, t0)}ms)")

    # Run part 2
    answer_2 = day_module.do_part_2(processed_input)
    t2 = datetime.now()
    print(f"Part 2: {answer_2} ({get_time_delta(t2, t1)}ms)")

    print(f"Done in {get_time_delta(t2, t0)}ms")


if __name__ == "__main__":
    run()
