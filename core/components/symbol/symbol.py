from dataclasses import dataclass
from datetime import datetime, timedelta

from API.yfinanceAPI.yfinance.yfinancesymbol import YfinanceSymbol as YfinanceSymbol
from core.components.symbol.utils.risk_reward import risk_reward_ratio
from core.components.symbol.utils.rsi import wilders_rsi
# from core.components.symbol.utils.doubles import get_local_maxima, get_local_minima
from core.components.symbol.utils.support_resistance_finder import support_resistance_finder, \
    min_support_and_max_resistance_prices


def yfinance_wrapper(func):
    def inner(*args, **kwargs):
        symbol = YfinanceSymbol(ticker=args[0].ticker, start_date=args[0].start_date, end_date=args[0].end_date)
        func(*args, symbol)

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
        pass

    @property
    def yahoo_api_obj(self):
        return YfinanceSymbol(ticker=self.ticker, start_date=self.start_date, end_date=self.end_date)

    @property
    @yfinance_wrapper
    def rsi(self, symbol: YfinanceSymbol):
        h = symbol.history(period='1y', interval='1d')
        h_close_prices = list(h.loc[:, 'Close'].values)
        rsi_values = wilders_rsi(data=h_close_prices, window_length=14)
        h['RSI'] = rsi_values

        return h['RSI']

    def support_resistance(self):
        return support_resistance_finder(self.ticker,
                                         start_date=self.start_date,
                                         end_date=self.end_date)


if __name__ == '__main__':
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    s = Symbol(ticker='AAPL', start_date=start_date, end_date=end_date)

    min_support_and_max_resistance_prices_df = min_support_and_max_resistance_prices(s.ticker, s.start_date, s.end_date)

    min_support_price = float(min_support_and_max_resistance_prices_df[min_support_and_max_resistance_prices_df["Support or Resistance"] == "Support"].Price)
    max_resistance_price = float(min_support_and_max_resistance_prices_df[min_support_and_max_resistance_prices_df["Support or Resistance"] == "Resistance"].Price)

    s_rrr = risk_reward_ratio(entry=s.yahoo_api_obj.current_price, target=max_resistance_price, stop=min_support_price)
    print(s_rrr)
