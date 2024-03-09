import logging.config
import logging.handlers
import pathlib
import json
import shlex

# import re
# import csv

# Use logger based on module name
logger = logging.getLogger(__name__)


def setup_logging():
    cwd = pathlib.Path.cwd()
    config_file = pathlib.Path(cwd, "logg_configs/config.json")
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)


# Solution for parse_file using re
# def parse_file(fname: str):
#     pattern = re.compile(r'("[^"]+"|\S+)')
#     commands = []
#     with open(fname, "r") as rfile:

#         for line in rfile:
#             result = pattern.findall(line)
#             print(result)
#     return commands


def parse_file(fname: str):
    commands = []
    with open(fname, "r") as rfile:
        for line in rfile:
            words = shlex.split(line)

            # Get command and parameters and log them to a file
            command = words[0]
            parameters = words.copy()
            parameters.pop(0)
            logger.info(f"Command: {command}, Parameters: {parameters}.")

            commands.append(words)
    return commands


def main() -> list:
    # Setup logging
    setup_logging()
    fname = "bank-records.txt"

    # Return a list of parsed records
    commands = parse_file(fname)
    return commands


if __name__ == "__main__":
    main()
