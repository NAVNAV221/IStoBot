import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

from consts.general.project import Consts

MRO_INDEX_FOR_FILTER_CHILD = -4


class Filter(ABC):
    """
    There are several filter methods.
    This class provide a basic structure to build multiple filter structure, such as screeners, analyst recommendation, and more ...
    """

    def __init__(self):
        self.check_filter_syntax()

        # Get filter type name (from the inherited class name)
        # self.filter_type = None
        self.input_data = self.parse_input()

    @property
    def filter_type(self):
        """
        Property that check in the JSON file if the input filter type match filter's class name
        :return:
        """
        filter_type_by_class = str(self._get_child_class_name()).lower()
        input_filter_type = str(list(self.input_data.get('filter_type', {}).keys())[0]).lower()
        if input_filter_type != filter_type_by_class:
            print(f"Input filter type from JSON doesn't Class filter name")
        return filter_type_by_class

    def _get_child_class_name(self):
        return self.__class__.mro()[MRO_INDEX_FOR_FILTER_CHILD].__name__

    def check_filter_syntax(self):
        """
        Check filter JSON syntax.
        """
        if not self.input_data.get('filter_type', False):
            raise Exception('JSON file miss filter type option')

    @staticmethod
    def parse_input() -> Dict:
        """
        Parse json input file from 'Input' folder and return a JSON data.
        """
        data = {}

        for json_input_file in os.listdir(Consts.PROJECT_JSON_INPUT_RELATIVE_PATH):

            if json_input_file.endswith('.json'):
                print(f"Identify input file: {json_input_file}")
                json_input_file_path = Path(Consts.PROJECT_JSON_INPUT_RELATIVE_PATH).joinpath(json_input_file)

                with open(json_input_file_path, 'r') as json_file:
                    data = json.load(json_file)
                    return data
        print('Unable to identify input file')
        return data

    @abstractmethod
    def parse_output(self):
        """
        Each platform have multiple outputs structures.
        :return:
        """
        pass
