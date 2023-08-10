from typing import List, Dict

from API.finvizAPI.finviz.screener import Screener as finviz_scanner_api
from bot.filters.screener.screener import Screener


class FinvizScreener(Screener):
    """
    Finviz - a stock platform we use to get data about stocks.
    There is a Github repo that provide access to their API.
    """

    def __init__(self, input_data: Dict = None):
        super().__init__(platform='finviz', input_data=input_data)

    @property
    def filters_api_format(self) -> List[str]:
        return self.extract_filters_value_from_user_input()

    def parse_input_by_platform(self):
        pass

    def format_filters(self) -> str:

        formatted_filters = []

        for filter_type, filter_value in self.filters.items():
            formatted_filters.append(f'{filter_type}: {filter_value}')
        filters_raw = "\n".join(formatted_filters)
        return filters_raw

    def get_matched_tickers(self) -> List[str]:
        """
        Get matched tickers by given JSON filters from Finviz API.
        """
        scanner_result = finviz_scanner_api(filters=self.filters_api_format, order='ticker')

        return scanner_result.tickers()

    def extract_filters_value_from_user_input(self):
        """
        Extract filters value from json user's input.

        JSON user input look come like this:
        "filters": {
            "Market Cap.": "+Small (over $300mln)"
        }
        We'll return only: cap_smallover, which is how Finviz API understand it

        :param filters_user_input:
        :return:
        """

        filters: List[str] = []
        finviz_api_filters = finviz_scanner_api.load_filter_dict()

        for user_filter_key, user_filter_value in self.screener_data['filters'].items():
            if not finviz_api_filters.get(user_filter_key):
                raise Exception(f"Finviz doesn't have the following key: {user_filter_key}")
            filters.append(finviz_api_filters[user_filter_key].get(user_filter_value))

        return filters


if __name__ == '__main__':
    input_data = {'filter_type': {'screener': {'screener_platform': 'FINVIZ', 'filters': {'Market Cap.': '+Small (over $300mln)'}}}}
    finviz_screener_one = FinvizScreener(input_data=input_data)

    channel_down_stock_list = finviz_scanner_api(filters=['ta_pattern_channeldown'])
    channel_up_stock_list = finviz_scanner_api(filters=['ta_pattern_channelup'])
    channel_up_down_stock_list = finviz_scanner_api(filters=['ta_pattern_channelup', 'ta_pattern_channeldown'])

    print(f"channel_down_stock_list length: {len(channel_down_stock_list)}")
    print(f"channel_up_stock_list length: {len(channel_up_stock_list)}")
    print(f"channel_up_down_stock_list length: {len(channel_up_down_stock_list)}")
    # print(finviz_screener_one.filters_api_format)
    #
    # matched_tickers = finviz_screener_one.get_matched_tickers()
    # print(matched_tickers)
    # print(finviz_screener.filters_api_format)
    # f = finviz_scanner_api(filters=finviz_screener.filters_api_format)

    # print(matched_tickers)
