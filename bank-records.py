import logging.config
import logging.handlers
import pathlib
import json
import re
import shlex
import csv

# Use loggers based on module names
logger = logging.getLogger(__name__)


def setup_logging():
    cwd = pathlib.Path.cwd()
    config_file = pathlib.Path(cwd, "logg_configs/config.json")
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)


# def parse_file_re(fname: str):
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
            logger.info(f"Command: {command}, Parameters: {parameters} ")

            commands.append(words)
    return commands


def main():
    # Setup logging
    setup_logging()
    # logger.info("info message")

    fname = "bank-records.txt"
    commands = parse_file(fname)
    for item in commands:
        print(item)


if __name__ == "__main__":
    main()
