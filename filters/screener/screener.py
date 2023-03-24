from abc import ABC, abstractmethod
from typing import Dict

from filters.filter import Filter


class Screener(Filter, ABC):
    """
    Screener is actually a filter for stocks that meet several criteria.
    """

    def __init__(self, platform: str):
        self.platform: str = platform
        self.input_data: Dict = self.parse_input()
        self.check_screener_syntax()

    @property
    def screener_data(self):
        """
        Return screener data
        """

        self._screener_data = self.input_data['filter_type']['screener']
        return self._screener_data

    @property
    def filters(self):
        """
        Return screener filters
        """

        return self.screener_data['filters']

    def check_screener_syntax(self):
        """
        Check whether input data has correct screener syntax.
        I don't trust the user he specified the correct platform syntax.
        Maybe instead of 'finviz' he spicified 'finiz' ...
        :return:
        """
        if not self.is_screener():
            raise Exception('Screener filter type not matched')
        if not self.is_input_platform_match():
            raise Exception('Unmatched input platform to the screener platform instance')

    def is_input_platform_match(self):
        if self.platform.lower() == str(self.screener_data['screener_platform']).lower():
            return True
        return False

    def is_screener(self) -> bool:
        """
        :return: true whether screener platform in the json input file. else false.
        """
        if str(self.filter_type).lower() == 'screener':
            print('Screener filter type identified')
            return True
        return False

    def get_screener_platform(self) -> str:
        return self.screener_data.get('screener_platform', None)

    def get_screener_filters(self) -> Dict:
        return self.screener_data.get('filters', None)

    @abstractmethod
    def parse_input_by_platform(self):
        """
        Each platform screener has different filter structure.
        Implementation is up to the platform program.
        """
        pass

    @abstractmethod
    def format_filters(self):
        """
        Each platform should format his filter and print them nicely.
        """
        pass

    def parse_output(self):
        pass
