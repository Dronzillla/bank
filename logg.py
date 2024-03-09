import logging.config
import logging.handlers
import pathlib
import json


def setup_logging() -> None:
    cwd = pathlib.Path.cwd()
    config_file = pathlib.Path(cwd, "logg_configs/config.json")
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)


def main() -> None:
    cwd = pathlib.Path.cwd()
    logg_dir = pathlib.Path(cwd, "logs")

    # Create logs in cwd if directory does not exist
    if not logg_dir.is_dir():
        pathlib.Path.mkdir(logg_dir)


if __name__ == "__main__":
    main()
