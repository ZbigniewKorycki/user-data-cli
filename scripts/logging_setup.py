import logging
import logging.config
import yaml


def setup_logging(logger_name):
    with open("../config/logging_config.yaml", "r") as f:
        config = yaml.safe_load(f.read())

    logging.config.dictConfig(config)
    logger = logging.getLogger(logger_name)
    return logger
