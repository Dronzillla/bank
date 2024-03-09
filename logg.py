import logging.config
import logging.handlers
import pathlib
import json


def setup_logging():
    cwd = pathlib.Path.cwd()
    config_file = pathlib.Path(cwd, "logg_configs/config.json")
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)


def main(): ...


if __name__ == "__main__":
    main()
