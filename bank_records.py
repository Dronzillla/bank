import logging.config
import logging.handlers
from logg import setup_logging
import shlex


# Use logger based on module name
logger = logging.getLogger(__name__)


def parse_file(fname: str) -> list[list]:
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
