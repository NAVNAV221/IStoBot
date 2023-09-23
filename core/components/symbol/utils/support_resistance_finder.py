from datetime import datetime, timedelta

import matplotlib.dates as mpl_dates
import numpy as np
import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr


# Calculate support and resistance levels


def is_support(df, i) -> bool:
    support = (
            df["Low"][i] < df["Low"][i - 1]
            and df["Low"][i] < df["Low"][i + 1]
            and df["Low"][i + 1] < df["Low"][i + 2]
            and df["Low"][i - 1] < df["Low"][i - 2]
    )
    return support


def is_resistance(df, i) -> bool:
    resistance = (
            df["High"][i] > df["High"][i - 1]
            and df["High"][i] > df["High"][i + 1]
            and df["High"][i + 1] > df["High"][i + 2]
            and df["High"][i - 1] > df["High"][i - 2]
    )
    return resistance


# Take out close support and resistance levels
def is_far_from_level(l, levels, s) -> bool:
    return np.sum([abs(l - x) < s for x in levels]) == 0


def support_resistance_finder(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    yf.pdr_override()

    # Retrieve the data from Yahoo Finance and create a pandas dataframe
    df = pdr.get_data_yahoo(ticker, start_date, end_date).reset_index()

    # Convert dates to matplotlib format
    df["Date"] = df["Date"].apply(mpl_dates.date2num)

    # Select the relevant columns
    df = df.loc[:, ["Date", "Open", "High", "Low", "Close"]]

    levels = []
    for i in range(2, df.shape[0] - 2):
        if is_support(df, i):
            levels.append((i, df["Low"][i]))
        elif is_resistance(df, i):
            levels.append((i, df["High"][i]))

    # Calculate the mean of the range of the stock price
    s = np.mean(df["High"] - df["Low"])

    # Add to list of levels
    levels = []
    for i in range(2, df.shape[0] - 2):
        if is_support(df, i):
            l = df["Low"][i]
            w = "Support"
            if is_far_from_level(l, levels, s):
                levels.append((i, l))
        elif is_resistance(df, i):
            l = df["High"][i]
            w = "Resistance"

            if is_far_from_level(l, levels, s):
                levels.append((i, l))

    # Identify dates and prices for each level
    dates = [x[0] for x in levels]
    prices = [x[1] for x in levels]

    # Identify support or resistance on each date
    which = []
    for date, price in zip(dates, prices):
        for i in range(2, df.shape[0] - 2):
            if price == df["Low"][i]:
                w = "Support"

            elif price == df["High"][i]:
                w = "Resistance"

            else:
                continue
        which.append(w)

    # Create and display dataframe with data
    new_dates = [start_date + timedelta(days=date) for date in dates]
    frame = pd.DataFrame(zip(new_dates, which, prices), columns=["Date", "Support or Resistance", "Price"]).set_index(
        "Date")
    return frame


def min_support_and_max_resistance_prices(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    support_resistance_frame = support_resistance_finder(ticker, start_date=start_date, end_date=end_date)

    result_df = pd.DataFrame

    if not support_resistance_frame.empty:
        # Filter the DataFrame to get "Support" rows
        support_df = support_resistance_frame[support_resistance_frame["Support or Resistance"] == "Support"]

        # Filter the DataFrame to get "Resistance" rows
        resistance_df = support_resistance_frame[support_resistance_frame["Support or Resistance"] == "Resistance"]

        if not support_df.empty and not resistance_df.empty:
            # Find the dataframe with the minimum "Price" in the "Support" group
            min_support = support_df[support_df.index == support_df["Price"].idxmin()]

            # Find the dataframe with the maximum "Price" in the "Resistance" group
            max_resistance = resistance_df[resistance_df.index == resistance_df["Price"].idxmax()]

            result_df = pd.concat([min_support, max_resistance], ignore_index=False)

    return result_df


if __name__ == '__main__':
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # support_resistance_frame = support_resistance_finder('AAPL', start_date=start_date, end_date=end_date)
    min_support_and_max_resistance_prices_dataframe = min_support_and_max_resistance_prices('AAPL',
                                                                                            start_date=start_date,
                                                                                            end_date=end_date)

    print(min_support_and_max_resistance_prices_dataframe)
