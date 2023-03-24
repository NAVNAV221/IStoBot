from typing import List

from API.finvizAPI.finviz.screener import Screener as finviz_scanner_api
from filters.screener.screener import Screener


class FinvizScreener(Screener):
    """
    Finviz - a stock platform we use to get data about stocks.
    There is a Github repo that provide access to their API.
    """

    def __init__(self):
        super().__init__(platform='finviz')

    def parse_input_by_platform(self):
        pass

    def format_filters(self) -> str:
        formatted_filters = []

        for filter_type, filter_value in self.filters.items():
            filters_key = list(filter_value.keys())
            formatted_filters_key = ", ".join(filters_key)
            formatted_filters.append(f'{filter_type}: {formatted_filters_key}')
        filters_raw = "\n".join(formatted_filters)
        return filters_raw

    def get_matched_tickers(self) -> List[str]:
        """
        Get matched tickers by given JSON filters from Finviz API.
        """
        scanner_result = finviz_scanner_api(filters=self.filters, order='ticker')

        return scanner_result.tickers()


if __name__ == '__main__':
    finviz_screener = FinvizScreener()
    # matched_tickers = finviz_screener.get_matched_tickers()
    # print(matched_tickers)
    print(finviz_screener.format_filters())
