import logging


def get_logger() -> None:
    """
    Set a Logic logger
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # define handler and formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # add formatter to handler
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)

    return logger