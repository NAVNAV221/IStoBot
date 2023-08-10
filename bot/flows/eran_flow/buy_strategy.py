from core.components.symbol import Symbol
from datetime import datetime, timedelta
import matplotlib.dates as mpdates
import pandas as pd

from API.yfinanceAPI.yfinance.symbol import Symbol
from API.yfinanceAPI.yfinance.symbol import Symbol
from core.components.symbol.utils.doubles import find_local_maximas_minimas, find_doubles_patterns


def main():
    start_date = datetime.now() - timedelta(days=120)
    end_date = datetime.now()
    # relevant_tickers = ['SCJ', 'FDEM', 'DFSE', 'DFAE', 'AADR', 'ONYX', 'SFWL', 'PCOR', 'MNST', 'EGP', 'PCGU', 'IX',
    #                     'AVEM', 'HY',
    #                     'CNTG', 'PANL', 'EQX']
    relevant_tickers = ['LQDH']

    for ticker in relevant_tickers:
        s = Symbol(ticker=ticker, start_date=start_date, end_date=end_date)
        s_history = s.history(period='1y', interval='1wk')


        # Find all the local minimas and maximas
        window_range = 10  # Defining the local range where min and max will be found
        max_min = find_local_maximas_minimas(s_history, window_range, smooth=True)
        print(max_min)

        # Find the tops and bottoms
        patterns_tops, patterns_bottoms = find_doubles_patterns(max_min)

        print(f"patterns_tops: {patterns_tops}\npatterns_bottoms: {patterns_bottoms}")


if __name__ == '__main__':
    main()
