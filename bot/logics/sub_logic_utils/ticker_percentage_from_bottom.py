from datetime import datetime
from API.yfinanceAPI.yfinance.symbol import Symbol
from bot.logics import Logic


class TickerPercentageFromBottom(Logic):
    @staticmethod
    def get_market_highest_price(symbol: Symbol) -> float:
        highest_price_number: float = 0.0

        print(symbol.highest_price)
        for date, price in symbol.highest_price.items():
            highest_price_date, highest_price_number = date, price
        return highest_price_number

    @staticmethod
    def get_current_market_price(symbol: Symbol):
        return symbol.current_price

    def main(self, market_ticker: str, start_date: datetime, end_date: datetime) -> float:
        market_symbol = Symbol(market_ticker, start_date=start_date, end_date=end_date)

        market_highest_price = self.get_market_highest_price(market_symbol)
        market_current_price = self.get_current_market_price(market_symbol)

        market_price_percent_from_highest = (market_highest_price / market_current_price) * 100

        return market_price_percent_from_highest
