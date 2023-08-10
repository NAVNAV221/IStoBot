from dataclasses import dataclass
from datetime import datetime, timedelta

from API.yfinanceAPI.yfinance.symbol import Symbol as YfinanceSymbol
from core.components.symbol.utils.rsi import wilders_rsi


def yfinance_wrapper(func):
    def inner(*args, **kwargs):
        symbol = YfinanceSymbol(ticker=args[0].ticker, start_date=args[0].start_date, end_date=args[0].end_date)
        func(args, symbol)

    return inner


@dataclass
class Symbol(object):
    """
    Future use in different project:
    s = Symbol(ticker='aapl')

    s.yfinance.info()
    s.finviz.current_price()
    """

    start_date: datetime
    end_date: datetime
    ticker: str

    def double_top(self):
        #     YfinanceSymbol(ticker=self.ticker)
        pass

    @property
    # @cached
    @yfinance_wrapper
    def rsi(self, symbol: YfinanceSymbol):
        h = symbol.history(period='1y', interval='1d')
        h_close_prices = list(h.loc[:, 'Close'].values)
        rsi_values = wilders_rsi(data=h_close_prices, window_length=14)
        h['RSI'] = rsi_values

        print(h['RSI'])
        return h['RSI']

    def risk_reward_ratio(self, entry: float, stop: float, target: float) -> float:
        risk_per_share = round(entry - stop, 2)
        reward_per_share = round(target - entry, 2)

        rrr = round(reward_per_share / risk_per_share, 2)

        return rrr


if __name__ == '__main__':
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    s = Symbol(ticker='AAPL', start_date=start_date, end_date=end_date)

    print(s.rsi)
