import logging
from abc import ABC
from uuid import uuid4


class Logic(ABC):
    """
    Logic define logical concept we want to run on our Bot.
    """

    def __init__(self):
        self._id = uuid4()
        self._set_logger()

    def main(self, **kwargs):
        """
        Logic main function.
        """
        raise NotImplementedError("Main function not implemented")

    def _set_logger(self) -> None:
        """
        Set a Logic logger
        """
        logger = logging.getLogger(self.__module__)
        logger.setLevel(logging.INFO)

        # define handler and formatter
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

        # add formatter to handler
        handler.setFormatter(formatter)

        # add handler to logger
        logger.addHandler(handler)

        self.logger = logger

    def run(self, **kwargs):
        """
        Function that runs Logic's main function.
        """
        return self.main(**kwargs)

if __name__ == '__main__':
    a = Logic()