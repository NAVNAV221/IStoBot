# Indicator Parameters
from datetime import datetime, timedelta

import numpy as np
import pandas

from API.yfinanceAPI.yfinance.yfinancesymbol import YfinanceSymbol
from core.components.symbol.utils.rsi import wilders_rsi

ALLOWED_RSI_CHANGE_GAP = 3

lookback = 13
lower_barrier = 30
upper_barrier = 70
width = 60


def adder(dataframe, times):
    for i in range(1, times + 1):
        new = np.zeros((len(dataframe), 1), dtype=float)
        dataframe = np.append(dataframe, new, axis=1)
    return dataframe


def signal(rsi_values: pandas.DataFrame, rsi_indicator_index, width, buy_index, sell_index):
    """

    :param rsi_values: RSI value
    :param rsi_indicator_index: The column to search for the Signal
    :param width: How far the algorithm will search within two peaks or troughs
    :param buy_index: Set to 1 if there was a buy signal action
    :param sell_index: Set to -1 if there was a sell signal action
    :return:
    """
    rsi_values = adder(rsi_values, 10)

    # Double bottom
    for i in range(len(rsi_values)):
        try:
            start_indicator_value = rsi_values[i, rsi_indicator_index]
            if start_indicator_value < lower_barrier:

                # Start to find the first trough
                for middle_value_index in range(i + 1, i + width):

                    # First trough
                    if rsi_values[middle_value_index, rsi_indicator_index] > lower_barrier:
                        for r in range(middle_value_index + 1, middle_value_index + width):

                            # Start to find the second trough
                            rsi_change_gap = rsi_values[r, rsi_indicator_index] - rsi_values[i, rsi_indicator_index]

                            if rsi_values[r, rsi_indicator_index] < lower_barrier and \
                                    rsi_values[
                                        r, rsi_indicator_index] >= start_indicator_value and rsi_change_gap < ALLOWED_RSI_CHANGE_GAP:

                                for s in range(r + 1, r + width):

                                    # Second trough - the point which surpass the lower barrier and set double booyom
                                    if rsi_values[s, rsi_indicator_index] > lower_barrier:
                                        rsi_values[s, buy_index] = 1
                                        break
                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break
        except IndexError:
            pass

    # Double top
    for i in range(len(rsi_values)):

        try:
            if rsi_values[i, rsi_indicator_index] > upper_barrier:

                for middle_value_index in range(i + 1, i + width):

                    # First trough
                    if rsi_values[middle_value_index, rsi_indicator_index] < upper_barrier:

                        for r in range(middle_value_index + 1, middle_value_index + width):
                            rsi_change_gap = rsi_values[i, rsi_indicator_index] - rsi_values[r, rsi_indicator_index]

                            if rsi_values[r, rsi_indicator_index] > upper_barrier and \
                                    rsi_values[r, rsi_indicator_index] <= rsi_values[
                                i, rsi_indicator_index] and rsi_change_gap < ALLOWED_RSI_CHANGE_GAP:

                                for s in range(r + 1, r + width):

                                    # Second trough
                                    if rsi_values[s, rsi_indicator_index] < upper_barrier:

                                        rsi_values[s, sell_index] = -1

                                        break

                                    else:
                                        break
                            else:
                                break
                        else:
                            break
                    else:
                        break

        except IndexError:
            pass

    return rsi_values


def main():
    start_date = datetime.now() - timedelta(days=360)
    end_date = datetime.now()

    s = YfinanceSymbol(ticker='AAPL', start_date=start_date, end_date=end_date)

    h = s.history(period='1y', interval='1d')
    h_close_prices = list(h.loc[:, 'Close'].values)

    rsi_values = wilders_rsi(data=h_close_prices, window_length=14)

    # doubles_bottom = signal(rsi_values=rsi_values, indicator_column=-1, )


# def func_test():
#     rsi_values = adder(rsi_values, 10)


if __name__ == '__main__':
    main()
