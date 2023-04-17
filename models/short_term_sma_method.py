import pandas as pd
import yfinance
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

COLUMN_AXIS = 1


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


def prepare_stock_to_backtest_class(ticker: str) -> pd.DataFrame:
    ticker_yahoo_object = yfinance.Ticker(ticker)
    ticker_history = ticker_yahoo_object.history(period="5y")
    prepared_ticker_history = ticker_history.drop(['Dividends', 'Stock Splits'], axis=COLUMN_AXIS)

    return prepared_ticker_history




def main():
    g = yfinance.Ticker('GOOG')
    x = prepare_stock_to_backtest_class('GOOG')
    print(x)
    bt = Backtest(x, SmaCross,
                  cash=10000, commission=.002,
                  exclusive_orders=True)
    output = bt.run()
    print(output)
    # bt.plot()


if __name__ == '__main__':
    main()
