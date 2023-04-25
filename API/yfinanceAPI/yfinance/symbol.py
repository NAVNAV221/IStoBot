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
