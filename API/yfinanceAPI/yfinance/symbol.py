from datetime import datetime, timedelta
from functools import cached_property, lru_cache
from typing import Dict, List

import yfinance as yf_package
from pandas import Series, DataFrame, Timestamp

from core.components.candle.candle import Candle


class Symbol(object):

    def __init__(self, ticker: str, start_date: datetime, end_date: datetime):
        self.ticker = ticker
        self.start_date: datetime = start_date,
        self.end_date: datetime = end_date,
        self.api_obj = yf_package.Ticker(self.ticker)

    @cached_property
    def info(self):
        return self.api_obj.info

    @cached_property
    def current_price(self) -> float:
        return self.api_obj.info.get('regularMarketPrice')

    @lru_cache
    def history(self, period='1y', interval='1wk', start_date: datetime = datetime.now() - timedelta(days=365),
                end_date: datetime = datetime.now()):
        return self.api_obj.history(start=start_date, end=end_date, period=period, interval=interval)

    def get_latest_double_top(self, period='1y'):
        pass

    @cached_property
    def highest_price(self, period='5y') -> Dict[Timestamp, float]:
        symbol_history = self.api_obj.history(period=period)
        symbol_close_history: Series = symbol_history['Close']

        highest_price_object: DataFrame = symbol_history.loc[symbol_close_history == max(symbol_close_history)]
        result = highest_price_object.iloc[0]

        close_price: float = result.Close
        close_price_date: Timestamp = result.name

        highest_price: Dict[Timestamp, float] = {close_price_date: close_price}

        return highest_price

    def resistance(self, start_date: datetime, end_date: datetime, reoccurrence: int,
                   minimum_deviation_number: float) -> List[
        List[
            DataFrame]]:
        """
        Check for resistance points in the stock history.

        :param minimum_deviation_number: Stock resistance price can play around price and still count as resistance level.
        :param end_date: end date to check for resistance.
        :param start_date: start date to check for resistance.
        :param reoccurrence: number of times the stock touch price, which we'll consider resistance.
        :return: List of stock history candles which present resistance.
        """
        candles_groups_price_delta: Dict[List[Candle, Candle]: float] = self.group_candle_between_price_delta(
            stock_history_candles=self.history(start_date=start_date, end_date=end_date),
            delta_price=minimum_deviation_number)
        avg_candles_groups_price = [(candle_pair[0].price + candle_pair[1].price) / 2 for candle_pair in
                                    candles_groups_price_delta.items()]
        resistance_points = {}

        for price in avg_candles_groups_price:
            other_price_index = avg_candles_groups_price.index(price) + 1
            resistance_points.update({price: []})

            for other_price in avg_candles_groups_price[other_price_index:]:
                if self.price_delta(other_price, price) <= minimum_deviation_number:
                    resistance_points.get(price).append(other_price)

        pass

    def support(self, start_date: datetime, end_date: datetime, reoccurrence: int, minimum_deviation: float) -> List[
        DataFrame]:
        """
        Check for support points in the stock history.

        :param minimum_deviation: Stock resistance price can play around price and still count as resistance level.
        :param end_date: end date to check for resistance.
        :param start_date: start date to check for resistance.
        :param reoccurrence: number of times the stock touch price, which we'll consider support.
        :return: List of stock history candles which present support.
        """
        pass

    @staticmethod
    def price_delta(price_1, price_2) -> float:
        return abs(price_1 - price_2)

    # TODO: Change stock_close_price_history to stock_history_candles: List[Candle]
    def group_candle_between_price_delta(self, stock_history_candles: DataFrame, delta_price: Union
    [float, int]) -> Dict[List[Candle, Candle]: float]:
        """
        Example:
        stock close price history: (10.1, 13.2, 11.3, 9.2, 14.3)
        {
            [10.1, 13.2]: 3.1,
            [10.1, 11.3]: 1.2,
            [10.1, 9.2]: 1.1,
            [10.1, 14.3]: 4.2,
            [13.2, 11.3]: 2.1,
            [13.2, 9.2]: 3,
            [13.2, 14.3]: 1.1,
            [11.3, 9.2]: 2.1,
            [11.3, 14.3]: 3,
            [9.2, 14.3]: 5.1
        }
        delta_price = 1.5,

        return value: [[10.1, 11.3], [10.1, 9.2], [13.2, 14.3]]
        {
            [10.1, 11.3]: 1.2,
            [10.1, 9.2]: 1.1,
            [13.2, 14.3]: 1.1
        }

        :param stock_history_candles: Stock candle history
        :param delta_price: Minimum delta price between each candle close price inside group.
        :return: List of group candles around the same close price.
        """
        start_index = 0
        candles_groups_price_delta: Dict[List[Candle, Candle]: float] = {}

        for i in stock_history_candles.index:
            start_index += 1
            first_stock_low_price = stock_history_candles['Low'][i]

            for j in stock_history_candles.index[start_index:]:
                second_stock_low_price = stock_history_candles['Low'][j]
                candle_pair_delta_price = self.price_delta(first_stock_low_price, second_stock_low_price)

                if candle_pair_delta_price <= delta_price:
                    candles_groups_price_delta.update(
                        {[first_stock_low_price, second_stock_low_price]: candle_pair_delta_price})

        return candles_groups_price_delta


if __name__ == '__main__':
    start_date = datetime.now() - timedelta(days=120)
    end_date = datetime.now()

    s = Symbol(ticker='WWE', start_date=start_date, end_date=end_date)

    h = s.history(period='1y', interval='1wk')

    h['Date'] = h.index

    print(h)

    # candle_groups_price_delta = s.group_candle_between_price_delta(stock_close_price_history=h, delta_price=1.5)
    # print(candle_groups_price_delta)
