from datetime import datetime
from importlib import import_module

import click


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

    # Run part 1
    answer_1 = day_module.do_part_1(blob)
    print(f"Part 1: {answer_1}")

    # Run part 2
    answer_2 = day_module.do_part_2(blob)
    print(f"Part 2: {answer_2}")

    print("done")


if __name__ == "__main__":
    run()
