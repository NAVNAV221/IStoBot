from datetime import datetime, timedelta
from typing import List

from pandas import DataFrame

from core.components.symbol import Symbol
from core.components.symbol.utils.doubles import get_last_double_top, get_last_double_bottom


def main():
    start_date = datetime.now() - timedelta(days=120)
    end_date = datetime.now()

    relevant_tickers = ['GOOG']

    for ticker in relevant_tickers:
        s = Symbol(ticker=ticker, start_date=start_date, end_date=end_date)

        double_top_candles: List[DataFrame] = get_last_double_top(symbol=s.yahoo_api_obj)
        print(f"double_top_candles: {double_top_candles}")

        double_bottom_candles: List[DataFrame] = get_last_double_bottom(symbol=s.yahoo_api_obj)
        print(f"double_bottom_candles: {double_bottom_candles}")

        double_top_candles_avg = double_top_candles['Close'].mean()
        print(f"double_top_candles_avg: {double_top_candles_avg}")

        double_bottom_candles_avg = double_bottom_candles['Close'].mean()
        print(f"double_bottom_candles_avg: {double_bottom_candles_avg}")

        print(f"entry: {s.yahoo_api_obj.current_price}", f"stop: {double_bottom_candles_avg}",
              f"target: {double_top_candles_avg}")
        risk_reward_ratio = s.risk_reward_ratio(entry=s.yahoo_api_obj.current_price, stop=double_bottom_candles_avg,
                                                target=double_top_candles_avg)
        print(f"risk_reward_ratio: {risk_reward_ratio}")


if __name__ == '__main__':
    main()
