# src/utils/logger.py
import logging
import sys


def setup_logger(name, level=logging.INFO):
    """Function to setup a logger with a Stream handler."""
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


logger = setup_logger("climate_risk_prediction", logging.INFO)
