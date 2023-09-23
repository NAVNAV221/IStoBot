"""
Date 20230105

This progam implements the Doubles Chart Patterns

Source: https://alpaca.markets/learn/algorithmic-trading-chart-pattern-python/
        https://github.com/samchaaa/alpaca_tech_screener/blob/master/tech_screener_notebook.ipynb
"""

from datetime import datetime, timedelta

import pandas as pd

from API.yfinanceAPI.yfinance.yfinancesymbol import YfinanceSymbol
# from core.components.symbol.symbol import Symbol


def get_last_double_top(symbol: YfinanceSymbol):
    """
    Return last two maxima points. Necessary columns are 'Date' and 'Close'
    :param maxima_candles: Maximan candles we found.
    :return: List of double top points.
    """
    s_history = symbol.history()

    maxima_candles = get_local_maxima(s_history)
    ordered_candles = maxima_candles.sort_values(by=['Date'], ascending=False)
    double_top_candles = ordered_candles['Close'].nlargest(2)

    double_top_candles = s_history.loc[double_top_candles.index]

    return double_top_candles


def get_last_double_bottom(symbol: YfinanceSymbol):
    """
    Return last two maxima points. Necessary columns are 'Date' and 'Close'
    :param maxima_candles: Maximan candles we found.
    :return: List of double top points.
    """
    s_history = symbol.history()

    minima_candles = get_local_minima(s_history)
    ordered_candles = minima_candles.sort_values(by=['Date'], ascending=False)
    print(f"ordered_candles: {ordered_candles}")
    double_buttom_candles = ordered_candles['Close'].nsmallest(2)

    double_buttom_candles = s_history.loc[double_buttom_candles.index]


    return double_buttom_candles


def get_local_maxima(stock_history: pd.DataFrame, windows_range: int = 5) -> pd.DataFrame:
    """
    Find local maxima extreme points in stock graph.
    :param stock_history: Stock data history. Necessary columns are: 'Close'.
    :param windows_range: Range which we check each candle.
    :return: List of maxima points.
    """
    # CHATGPT
    # Define the rolling window size (number of periods to consider)
    rolling_window = windows_range

    ohlc = stock_history

    # Calculate the rolling maximum of 'Close'
    ohlc['Rolling_Max_Close'] = ohlc['Close'].rolling(window=rolling_window, center=True).max()

    # Identify local maxima points within the rolling window
    ohlc['Local_Maxima'] = (ohlc['Close'] == ohlc['Rolling_Max_Close'])

    # Filter out rows where local maxima are False
    local_maxima_points = ohlc[ohlc['Local_Maxima']]

    return local_maxima_points


def get_local_minima(stock_history: pd.DataFrame, windows_range: int = 5) -> pd.DataFrame:
    """
    Find local minimas extreme points in stock graph.
    :param stock_history: Stock data history. Necessary columns are: 'Close'.
    :param windows_range: Range which we check each candle.
    :return: List of minimas points.
    """
    # CHATGPT
    # Define the rolling window size (number of periods to consider)
    rolling_window = windows_range

    ohlc = stock_history
    # Calculate the rolling maximum of 'Close'
    ohlc['Rolling_min_Close'] = ohlc['Close'].rolling(window=rolling_window, center=True).min()

    # Identify local minima points within the rolling window
    ohlc['Local_minima'] = (ohlc['Close'] == ohlc['Rolling_min_Close'])

    # Filter out rows where local minima are False
    local_minima_points = ohlc[ohlc['Local_minima']]

    return local_minima_points


if __name__ == "__main__":
    start_date = datetime.now() - timedelta(days=360)
    end_date = datetime.now()
    ticker = 'GOOG'

    s = YfinanceSymbol(ticker=ticker, start_date=start_date, end_date=end_date)
    print(get_last_double_bottom(s))
