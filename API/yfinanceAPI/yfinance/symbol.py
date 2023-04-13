import pandas as pd
import yfinance as yf_package

from datetime import datetime
from typing import Dict
from pandas import Series, DataFrame, Timestamp


class Symbol(object):
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.api_obj = yf_package.Ticker(self.ticker)

    @property
    def info(self):
        return self.api_obj.info

    @property
    def current_price(self) -> float:
        return self.api_obj.info.get('regularMarketPrice')

    def history(self, period='5y', interval='1mo') -> pd.DataFrame:
        return self.api_obj.history(period=period, interval=interval)

    def get_highest_price(self, period='5y') -> Dict[Timestamp, float]:
        symbol_history = self.api_obj.history(period=period)
        symbol_close_history: Series = symbol_history['Close']

        highest_price_object: DataFrame = symbol_history.loc[symbol_close_history == max(symbol_close_history)]
        result = highest_price_object.iloc[0]

        close_price: float = result.Close
        close_price_date: Timestamp = result.name

        highest_price: Dict[Timestamp, float] = {close_price_date: close_price}

        return highest_price



if __name__ == '__main__':
    msft = Symbol(ticker='MSFT')
    print(msft.current_price)
    res = msft.get_highest_price()

    for k, v in res.items():
        print(v)
    # msft = yf_package.Ticker("MSFT")
    # # get all stock info (slow)
    # msft.info
    # # fast access to subset of stock info (opportunistic)
    # msft.fast_info
    #
    # # get historical market data
    # hist = msft.history(period='5y', interval='1mo')
    # print(hist.iterrows())
