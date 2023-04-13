from pathlib import Path


class Consts:
    PROJECT_ROOT_PATH = Path(r'c:\Users\navnav221\PycharmProjects\IStoBot')
    PROJECT_FILTERS_RELATIVE_PATH = Path(r'filters')
    PROJECT_JSON_INPUT_RELATIVE_PATH = PROJECT_ROOT_PATH.joinpath(PROJECT_FILTERS_RELATIVE_PATH.joinpath('Input'))
