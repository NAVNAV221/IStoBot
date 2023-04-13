from API.yfinanceAPI.yfinance import Symbol
from Logics import Logic
from inspect import signature


class BearMarketLogic(Logic):
    @staticmethod
    def get_market_highest_price(symbol: Symbol) -> float:
        highest_price_number: float = 0.0

        for date, price in symbol.get_highest_price().items():
            highest_price_date, highest_price_number = date, price
        return highest_price_number

    @staticmethod
    def get_current_market_price(symbol: Symbol):
        return symbol.current_price

    def main(self, market_ticker: str) -> bool:
        market_symbol = Symbol(market_ticker)

        market_highest_price = self.get_market_highest_price(market_symbol)
        market_current_price = self.get_current_market_price(market_symbol)

        market_price_percent_from_highest = (market_highest_price / market_current_price) * 100

        if market_price_percent_from_highest > 120:
            self.logger.info(f'Bear market with market_price_percent_from_highest: {market_price_percent_from_highest}')
            return True

        self.logger.info(f'Not bear market with market_price_percent_from_highest: {market_price_percent_from_highest}')
        return False


if __name__ == '__main__':
    b = BearMarketLogic()
    c = b.run
    print(signature(b.run))
    # b.run(ticker='MSFT')
